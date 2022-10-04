kubectl delete -f jenkins_svc.yaml 

kubectl delete -f jenkins_deploy.yaml

kubectl delete -f jmeter_slaves_svc.yaml

kubectl delete -f jmeter_slaves_configmap.yaml

kubectl delete -f jmeter_slaves_deploymentconfig.yaml

kubectl delete -f influxdb_svc.yaml

kubectl delete -f influxdb_deploymentconfig.yaml

kubectl delete -f influxdb_configmap.yaml

kubectl delete -f grafana_deploy.yaml

kubectl delete -f jmeter_master_configmap.yaml

kubectl delete -f jmeter_master_deploymentconfig.yaml

kubectl delete -f jenkins-pvc.yaml

kubectl delete -f influxdb-pvc.yaml

kubectl delete -f grafana-pvc.yaml

kubectl delete svc jenkins

kubectl delete svc jmeter-grafana
