values_file=minio/values.yaml
values_env_file=minio/values_with_env.yaml
job_file=minio/create_bucket_job.yaml
job_file_with_env=minio/create_bucket_job_env.yaml
service_file=minio/service.yaml
service_file_with_env=minio/service_env.yaml

if [ ! -f "$values_file" ]; then
  echo "El archivo $values_file no existe."
  exit 1
fi


envsubst < "$values_file" > "$values_env_file"
envsubst < "$job_file" > "$job_file_with_env"
envsubst < "$service_file" > "$service_file_with_env"


# Verificar si ya existe un despliegue de Helm llamado "mlflow"
if helm status minio -n ${MINIO_NAMESPACE} >/dev/null 2>&1; then
    echo "El despliegue de Helm 'minio' ya existe."
else
    echo "El despliegue de Helm 'minio' no existe. Realizando la instalación..."
    helm install prometheus prometheus-community/prometheus-operator-crds

    # Verificar si el archivo values.yaml existe
    if [ ! -f "$values_env_file" ]; then
        echo "El archivo $values_env_file no existe."
        exit 1
    fi

    # Instalar el despliegue de Helm "minio" con valores personalizados desde values.yaml
    helm install minio bitnami/minio --namespace ${MINIO_NAMESPACE} --create-namespace --values "$values_env_file"

    # Esperar a que todos los pods estén en estado "Running"
    echo "Esperando a que todos los pods estén en estado 'Running'..."

    kubectl wait pod --all --for=condition=Ready --namespace=${MINIO_NAMESPACE}

    kubectl apply -f $job_file_with_env
    kubectl apply -f $service_file_with_env

    echo "El despliegue de Helm 'minio' se ha instalado con éxito."
fi