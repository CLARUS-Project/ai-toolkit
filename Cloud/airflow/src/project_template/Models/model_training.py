"""
This module defines the `model_training` function used by the pipeline orchestrator to train a machine 
learning model using ElasticNet regularization. This function defines the logic for training the model and evaluating 
its performance.

Any additional functions or utilities required for this step can be defined within this script itself or split into 
different scripts and included in the Process directory.
"""


from typing import Dict, Any
from sksurv.ensemble import RandomSurvivalForest
import numpy as np
import mlflow
import mlflow.sklearn
from mlflow.tracking.client import MlflowClient
from urllib.parse import urlparse
import config
import time
import warnings
from sksurv.metrics import (
    as_concordance_index_ipcw_scorer,
    as_cumulative_dynamic_auc_scorer,
    as_integrated_brier_score_scorer,
    cumulative_dynamic_auc,
    integrated_brier_score
)
from utils import track_run

def model_training(data: Dict[str, Any]):
    """
    Args:
        data: A dictionary containing the preprocessed data.

    Returns:
        None
    """

    test_min = data['test_labels']['survival_in_minutes'].min()
    test_max = data['test_labels']['survival_in_minutes'].max()
    train_min = data['train_labels']['survival_in_minutes'].min()
    train_max = data['train_labels']['survival_in_minutes'].max()
    ntimes = 30
    test_va_times = np.arange(test_min, test_max, (test_max - test_min) / ntimes)
    train_va_times = np.arange(train_min, train_max, (train_max - train_min) / ntimes)
    threads = 8

    # Model training
    estimator_name = 'Survival Random Forest'
    for N in [5]:
        for n_trees in [100]:
            for min_leafs in [10]:
                run_name = f'N={N}, n_trees={n_trees}, min samples leaf={min_leafs}'
                hyperparameters = {'n_estimators': n_trees, 'min_samples_leaf': min_leafs, 'N':N}
                tr_metrics = dict()
                val_metrics = dict()

                model = RandomSurvivalForest(n_estimators=n_trees, min_samples_leaf=min_leafs, n_jobs=threads, random_state=4)
                model = as_concordance_index_ipcw_scorer(model)
                print('Training model')
                model.fit(data['train_data'], data['train_labels'])
                print('Training finished')
                train_score = model.score(data['train_data'], data['train_labels'])
                val_score = model.score(data['test_data'], data['test_labels'])
                tr_metrics['Train concordance index ipcw'] = train_score
                val_metrics['Validation concordance index ipcw'] = val_score
                print(train_score, val_score)

                #Integrated Brider Score
                distrib = np.concatenate((data['train_labels'], data['test_labels']), axis=0)
                #Train Integrated Brider Score
                surv_prob = []
                for fn in model.predict_survival_function(data['train_data']):
                    surv_prob.append(fn(train_va_times))
                train_ibs = integrated_brier_score(distrib, data['train_labels'], surv_prob, train_va_times)
                tr_metrics['train integrated brier score'] = train_ibs

                # Test Integrated Brider Score
                surv_prob = []
                for fn in model.predict_survival_function(data['test_data']):
                    surv_prob.append(fn(test_va_times))
                test_ibs = integrated_brier_score(distrib, data['test_labels'], surv_prob, test_va_times)
                val_metrics['test integrated brier score'] = test_ibs

                # Mean auc train and val scores
                risk_scores = model.predict(data['test_data'])
                _, mean_auc = cumulative_dynamic_auc(data['train_labels'], data['test_labels'], risk_scores, test_va_times)
                val_metrics['mean auc'] = mean_auc

                # Track the run
                track_run(run_name, estimator_name, hyperparameters, tr_metrics, val_metrics, model)
