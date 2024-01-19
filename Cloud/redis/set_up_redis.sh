#!/bin/bash
helm repo add bitnami https://charts.bitnami.com/bitnami

values_file=redis/values.yaml
values_env_file=redis/values_with_env.yaml

# Sustitución de las variables en values.yaml
if [ ! -f "$values_file" ]; then
  echo "El archivo $values_file no existe."
  exit 1
fi

envsubst < "$values_file" > "$values_env_file"

# Verificar si ya existe un despliegue de Helm llamado "mlflow"
if helm status redis -n ${REDIS_NAMESPACE} >/dev/null 2>&1; then
    echo "El despliegue de Helm 'redis' ya existe."
else
    echo "El despliegue de Helm 'redis' no existe. Realizando la instalación..."

    # Verificar si el archivo values.yaml existe
    if [ ! -f "$values_env_file" ]; then
        echo "El archivo $values_env_file no existe."
        exit 1
    fi

    # Instalar el despliegue de Helm "mlflow" con valores personalizados desde values.yaml
    helm install redis bitnami/redis --namespace ${REDIS_NAMESPACE} --create-namespace --values "$values_env_file"

    echo "El despliegue de Helm 'redis' se ha instalado con éxito."
fi