helm delete -n mlflow mlflow
helm delete -n airflow airflow
helm delete -n minio minio
helm delete -n default prometheus
helm delete -n redis redis

kubectl delete -n minio -f minio/service.yaml
kubectl delete -n mlflow -f mlflow/service.yaml

kubectl delete pvc --all -A

kubectl delete -f airflow/postgres_service_env.yaml
kubectl delete -f minio/service_env.yaml
kubectl delete -f mlflow/service_env.yaml

/usr/local/bin/k3s-uninstall.sh
