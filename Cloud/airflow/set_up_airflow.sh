#!/bin/bash

values_file=airflow/values.yaml
values_env_file=airflow/values_with_env.yaml
job_file=airflow/create_db_job.yaml
job_file_with_env=airflow/create_db_job_env.yaml
service_file=airflow/postgres_service.yaml
service_file_with_env=airflow/postgres_service_env.yaml

# Sustitución de las variables en values.yaml
if [ ! -f "$values_file" ]; then
  echo "El archivo $values_file no existe."
  exit 1
fi

# echo ${MINIO_CONN}
MINIO_CONN=$(echo -n "$MINIO_CONN" | base64 | sed ':a;N;$!ba;s/\n//g')

envsubst < "$values_file" > "$values_env_file"
envsubst < "$job_file" > "$job_file_with_env"
envsubst < "$service_file" > "$service_file_with_env"

# Verificar si ya existe un despliegue de Helm llamado "mlflow"
if helm status airflow -n ${AIRFLOW_NAMESPACE} >/dev/null 2>&1; then
    echo "El despliegue de Helm 'airflow' ya existe."
else
    echo "El despliegue de Helm 'airflow' no existe. Realizando la instalación..."

    # Verificar si el archivo values.yaml existe
    if [ ! -f "$values_env_file" ]; then
        echo "El archivo $values_env_file no existe."
        exit 1
    fi

    # Instalar el despliegue de Helm "mlflow" con valores personalizados desde values.yaml
    helm upgrade --install airflow apache-airflow/airflow --namespace ${AIRFLOW_NAMESPACE} --create-namespace --values "$values_env_file"

    kubectl apply -f $job_file_with_env
    kubectl apply -f $service_file_with_env

    echo "El despliegue de Helm 'airflow' se ha instalado con éxito."
fi