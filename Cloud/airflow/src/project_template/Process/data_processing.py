"""
This module defines the data_processing function used by the pipeline orchestrator to perform data preprocessing. 
This function defines the logic for data preprocessing. Any adidtional function needed to perform this step can 
be defined within this script itself or split into different scripts and included in the Process directory.
"""


from sklearn.model_selection import train_test_split
from typing import Dict, Any
import pandas as pd
import numpy as np


def data_processing(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform data preprocessing on the input dataframe and transform it into train and validation datasets.

    In this code example, the input dataframe is divided into train_x, train_y, val_x and val_y dataframes.

    Args:
        df: The input dataframe containing the data to be preprocessed.

    Return:
        A dictionary containing the preprocessed data.
    """

    samples = df.iloc[:, :-2]
    labels = df.iloc[:,-2:]
    samples, labels = transform_dataset(samples, labels)

    train_data, test_data, train_labels, test_labels = train_test_split(samples, labels, train_size=0.8)

    return {'train_data': train_data, 'test_data': test_data, 'train_labels': train_labels, 'test_labels': test_labels}


def transform_dataset(frame, labels, features=['stdMeter', 'lastNStd', 'lastNMeter', 'longEwa'], N=6, lower_limit=5,
                      sensor=34, censor=False, delete_nulls=True, upper_limit=1700, verbose=False):
    '''
    :param frame: DataFrame with all features
    :param labels: Dataframe with columns 'status' and 'survivalInMinutes'
    :param features: Available features:
        -meterMean: Mean of each sensor's measures
        -longEwa: Long exponential weighted average of the meter
        -shortEwa: Short exponential weighted average
        -stdMeter: Meter's Standard deviation within a timeframe
        -lastNMeter: Last N values read
        -lastNAcumMeter: Last N acumulated meter values
        -lastNMean: Mean of the last N measures
        -lastNStd: Standard deviation of the last N measures
    :param N: Number of measures collected before failure/censor
    :param lower_limit: Minimum number of minutes in between data points
    :param sensor: No editable. numero de sensores de los que se recogen valores.----------------------------------------------------------
    :param censor: Censor data that is not separated for at least time_margin minutes
    :param upper_limit: Maximum survival length duration -> To delete outliers
    :param delete_nulls: Delete data points that contain one or more nulls. Number of data points will be printed before and after
    :param verbose: Print the number of datapoints
    :return: (dataspoints_df, labels) with last N measures, de los sensor/es separados por time_margin minutos-------------------------------
    '''

    # Delete/censor datapoints which survival time < time_margin or > upperClean
    dont_remove = labels.iloc[:, 1] >= lower_limit
    if upper_limit > 0:
        dont_remove = dont_remove & (labels.iloc[:, 1] <= upper_limit)

    # Eliminate or censor the datapoints
    if censor:
        labels.iloc[1][~dont_remove] = False
    else:
        labels = labels[dont_remove]
        frame = frame[dont_remove]

    cols = []
    special = []
    # Process required features
    for feature in features:
        if feature in ['lastNMean', 'lastNStd']:
            special.append(feature)
            last = frame.loc[:,
                   [f"lastNMeter{j + 1} t-{i + 1}" for i in range(N) for j in range(min(sensor, 51)) if j != 28]].copy()
        elif feature in ['lastNAcumMeter', 'lastNMeter']:
            cols += [feature + f"{j + 1} t-{i + 1}" for i in range(N) for j in range(min(sensor, 51)) if j != 28]
        else:
            cols += [feature + f'{j + 1}' for j in range(min(sensor, 51)) if j != 28]

    # Select the features from the dataset
    frame = frame.loc[:, cols]

    # Calculate special features
    aux = [[f"lastNMeter{j + 1} t-{i + 1}" for i in range(N)] for j in range(min(sensor, 51)) if j != 28]
    if 'lastNMean' in special:
        for i, contador in enumerate(aux):
            frame[f'lastNMean{i + 1 if i < 28 else i + 2}'] = last.loc[:, contador].mean(axis=1)
    if 'lastNStd' in special:
        for i, contador in enumerate(aux):
            frame[f'lastNStd{i + 1 if i < 28 else i + 2}'] = last.loc[:, contador].std(axis=1)
    frame.reset_index(inplace=True, drop=True)
    labels.reset_index(inplace=True, drop=True)

    if verbose:
        print(len(frame))

    # Delete nulls if necessary
    if delete_nulls:
        dont_remove = pd.notnull(frame).all(axis=1)
        frame = frame.loc[dont_remove]
        labels = labels.loc[dont_remove]
        if verbose:
            print(len(frame))

    # Transform labels into a structured array
    labels = np.array([x for x in zip(labels['status'], labels['survivalInMinutes'])],
                      dtype=[('status', 'bool'), ('survival_in_minutes', '<f4')])
    return frame, labels