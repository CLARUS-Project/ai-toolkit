#!/bin/bash

# Comprueba si kubectl está instalado
if ! kubectl cluster-info &> /dev/null; then
    echo "El cluster no esta en funcionamiento. Instalando..."
    # exit 1

    curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server" sh -s - --write-kubeconfig-mode=644
    sudo chmod 777 /etc/rancher/k3s/k3s.yaml
    sudo mkdir -p ~/.kube/
    sudo cp /etc/rancher/k3s/k3s.yaml ~/.kube/config

fi

# Comprueba si Kubernetes está en funcionamiento
if kubectl cluster-info &> /dev/null; then
    echo "Kubernetes instalado correctamente..."
else
    echo "Kubernetes no está en funcionamiento. Verifica que tu clúster esté activo antes de ejecutar este script."
    exit 1
fi

if ! command -v helm &> /dev/null; then
    echo "Helm no está instalado. Instalando Helm..."

    # Descargar e instalar Helm
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh

    echo "Helm ha sido instalado correctamente."
else
    echo "Helm ya está instalado. No es necesario realizar ninguna acción."
fi

env_file=.env

# Verifica si el archivo .env existe
if [ ! -f "$env_file" ]; then
    echo "El archivo $env_file no existe.\n"
    exit 1
fi

# Lee el archivo .env y exporta las variables de entorno
set -a
. ./${env_file}
set +a

# Muestra un mensaje de confirmación
echo "Variables de entorno exportadas desde $env_file."

# Preparar Kubernetes

helm repo add community-charts https://community-charts.github.io/helm-charts
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add apache-airflow https://airflow.apache.org

helm repo update

./minio/set_up_minio.sh
./airflow/set_up_airflow.sh
./mlflow/set_up_mlflow.sh
./redis/set_up_redis.sh
