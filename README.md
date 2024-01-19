# AI TOOLKIT

The AI TOOLKIT is designed to effectively manage the entire life cycle of the models. To achieve this, we have implemented a set of containerised services (the Cloud part over Kubernetes and the Edge on Docker) that cater to various needs. The overall infrastructure is divided into two distinct projects, ensuring easier maintenance and independent implementations:

* **Cloud:** A set of services including Airflow, Mlflow, Postgres and others. The platform is deployed on Kubernetes, thus achieving greater flexibility with respect to Docker. The deployment is prepared so that by executing a script the platform can be installed.
* **Edge:** This Docker Compose project offers a comprehensive suite of AI toolkits designed for ML model inference at the edge, all accessible through a web API.

Both projects are thoroughly documented, offering clear installation and usage instructions, which can be found in the accompanying `README.md` files available in their respective folders.

## Installation Steps:

1. Clone the source code from the GitHub repository. You can achieve this by running the following command:

```
git clone <repository_url>
```
2. Change to the Cloud directory and follow the steps described in [README.md](Cloud/README.md)
   
3. Build and start the docker compose of the **Edge** project following the instrucctions given in the [README.md](Edge/README.md) of `Edge` directory.

**(optional) Integration with IDS**

4. Clone the source code from the [clarus_edge_deploy](https://github.com/CLARUS-HE-Project/true-connector-trainning/tree/master) repository and follow the instrucctions given in the [README.md](https://github.com/CLARUS-HE-Project/clarus_edge_deploy/blob/master/README.md)
5. 
6. Clone the source code from the [true-connector-trainning](https://github.com/CLARUS-HE-Project/clarus_edge_deploy) repository and follow the instrucctions given in the [README.md](https://github.com/CLARUS-HE-Project/true-connector-trainning/blob/master/README.md)