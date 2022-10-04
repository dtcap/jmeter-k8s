FOR /F "usebackq" %%i IN (`minikube ip`) DO SET K8S_IP=%%i
ECHO %K8S_IP%

@FOR /f "tokens=*" %%i IN ('minikube -p minikube docker-env --shell cmd') DO @%%i

docker build -t jenkins -f Dockerfile-jenkins --build-arg CLUSTER_IP=%K8S_IP% .

docker build -t jmeter-base -f Dockerfile-base .

docker build -t jmeter-master -f Dockerfile-master .

docker build -t jmeter-slave -f Dockerfile-slave .

kubectl create -f jenkins-pvc.yaml

kubectl create -f jenkins_deploy.yaml

kubectl create -f jenkins_svc.yaml 

kubectl expose deployment jenkins --port=8080 --external-ip=%K8S_IP% --type=NodePort

kubectl create -f jmeter_slaves_deploymentconfig.yaml

kubectl create -f jmeter_slaves_svc.yaml

kubectl create -f influxdb-pvc.yaml

kubectl create -f influxdb_configmap.yaml

kubectl create -f influxdb_deploymentconfig.yaml

kubectl create -f influxdb_svc.yaml

kubectl create -f grafana-pvc.yaml

kubectl create -f grafana_deploy.yaml

kubectl expose deployment jmeter-grafana --port 3000 --external-ip=%K8S_IP% --type NodePort

kubectl create -f jmeter_master_configmap.yaml

kubectl create -f jmeter_master_deploymentconfig.yaml

start "" http://%K8S_IP%:8080