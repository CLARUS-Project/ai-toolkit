#!/bin/bash

values_file=mlflow/values.yaml
values_env_file=mlflow/values_with_env.yaml
service_file=mlflow/service.yaml
service_file_with_env=mlflow/service_env.yaml

# Sustitución de las variables en values.yaml
if [ ! -f "$values_file" ]; then
  echo "El archivo $values_file no existe."
  exit 1
fi

kubectl create ns monitoring
envsubst < "$values_file" > "$values_env_file"
envsubst < "$service_file" > "$service_file_with_env"


# Verificar si ya existe un despliegue de Helm llamado "mlflow"
if helm status mlflow -n ${MLFLOW_NAMESPACE} >/dev/null 2>&1; then
    echo "El despliegue de Helm 'mlflow' ya existe."
else
    echo "El despliegue de Helm 'mlflow' no existe. Realizando la instalación..."

    # Verificar si el archivo values.yaml existe
    if [ ! -f "$values_env_file" ]; then
        echo "El archivo $values_env_file no existe."
        exit 1
    fi

    # Instalar el despliegue de Helm "mlflow" con valores personalizados desde values.yaml
    helm install mlflow community-charts/mlflow --namespace ${MLFLOW_NAMESPACE} --create-namespace --values "$values_env_file"

    kubectl apply -f $service_file_with_env

    echo "El despliegue de Helm 'mlflow' se ha instalado con éxito."
fi