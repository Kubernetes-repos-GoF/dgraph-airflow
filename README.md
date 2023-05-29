# dgraph-airflow

## Install Guide - cluster kubernetes GCP

gcloud auth login
gcloud config set project tf-my-gcp

gcloud container clusters create cluster-dgraph-air --zone us-west1-c --project tf-my-gcp --machine-type e2-standard-2

gcloud container clusters get-credentials cluster-dgraph-air --zone us-west1-c --project tf-my-gcp

------------------
kubectl create ns dgraph

helm repo add dgraph https://charts.dgraph.io
helm install dgraph-release --values ipwhitelist.yaml dgraph/dgraph -n dgraph --create-namespace

kubectl get pod -n dgraph
kubectl get pvc -n dgraph
kubectl get svc -n dgraph

kubectl port-forward service/dgraph-release-dgraph-alpha 8080:8080 -n dgraph

https://play.dgraph.io/?latest#
Dgraph Server Connection
http://localhost:8080

http://localhost:8080/state


helm install kube-prometheus-stack --values dgraph_prometheus_v4.yml,dgraph-backup-alert-rules.yml,dgraph-app-alert-rules.yml --set grafana.adminPassword='andysanru' prometheus-community/kube-prometheus-stack --namespace dgraph

kubectl get pod -n dgraph
kubectl get svc -n dgraph
-- Search external IP: kube-prometheus-stack-grafana and Open in Browser, Ex: 35.222.242.72
Usr: admin
Pwd: andysanru


------------------
kubectl create ns airflow

helm repo add apache-airflow https://airflow.apache.org
helm install airflow-release apache-airflow/airflow -n airflow --debug

kubectl get pod -n airflow
kubectl get pvc -n airflow
kubectl get svc -n airflow


kubectl port-forward svc/airflow-release-webserver 8081:8080 -n airflow

http://localhost:8081
Usr: admin
Pwd: admin

helm show values apache-airflow/airflow > airflow-values-yaml
helm ls -n airflow

helm upgrade --install airflow-release apache-airflow/airflow -n airflow -f airflow-values-yaml --debug
helm ls -n airflow

kubectl get pod -n airflow





// kubectl exec --stdin --tty  -n airflow -- /bin/bash



------- Dgraph live

k cp /home/andres/Documents/work/dk/dgraph-airflow/data/. dgraph-release-dgraph-alpha-0:p/ -n dgraph

kubectl exec -it dgraph-release-dgraph-alpha-0 -n dgraph -- sh


dgraph live -f ./data/family.rdf -s ./data/family.schema --format=rdf --zero=dgraph-release-dgraph-zero-0.dgraph-release-dgraph-zero-headless.dgraph.svc.cluster.local:5080 --alpha=localhost:9080 --logtostderr


kubectl exec -it dgraph-release-dgraph-alpha-0 -n dgraph -- dgraph live -f ./data/family.rdf -s ./data/family.schema --format=rdf --zero=dgraph-release-dgraph-zero-0.dgraph-release-dgraph-zero-headless.dgraph.svc.cluster.local:5080 --alpha=localhost:9080 --logtostderr


{
  movie(func:eq(name, "Homer"))
  {
    name
    parent_to{
			name
    }
  }
}



------- Dgraph bulk

kubectl exec -it dgraph-release-dgraph-zero-0 -n dgraph -- sh

apt-get update
apt-get install -y wget file

wget -q -O 1million.schema  "https://github.com/dgraph-io/benchmarks/blob/master/data/1million.schema?raw=true"
wget -q -O 1million.rdf.gz  "https://github.com/dgraph-io/benchmarks/blob/master/data/1million.rdf.gz?raw=true"


dgraph bulk -f 1million.rdf.gz -s 1million.schema --map_shards=1 --reduce_shards=1 --http localhost:8000 --zero=localhost:5080

kubectl cp dgraph-release-dgraph-zero-0:out/. /home/andres/Documents/work/dk/dgraph-airflow/out/ -n dgraph

-- Repita para alpha-1 y alpha-2
kubectl exec -it dgraph-release-dgraph-alpha-0 -n dgraph -- sh

rm -rf p
mkdir p
chmod 700 p

-- Copy files to Alpha Pods
kubectl cp /home/andres/Documents/work/dk/dgraph-airflow/out/0/p/. dgraph-release-dgraph-alpha-0:p/ -n dgraph
kubectl cp /home/andres/Documents/work/dk/dgraph-airflow/out/0/p/. dgraph-release-dgraph-alpha-1:p/ -n dgraph
kubectl cp /home/andres/Documents/work/dk/dgraph-airflow/out/0/p/. dgraph-release-dgraph-alpha-2:p/ -n dgraph


-- Restart server
watch kubectl get pod -n dgraph
kubectl logs -f dgraph-release-dgraph-alpha-0 -n dgraph

http://localhost:8080/admin/shutdown


-- Check Schema and Query
https://play.dgraph.io/?latest#

{
  movie(func:alloftext(name@de, "Die schwarz"))
    @filter(has(genre))
  {
    name@de
    name@en
    name@it
  }
}



---------------------------------------------------
--- Airflow Notes
Default Postgres connection credentials:
    username: postgres
    password: postgres
    port: 5432


You can get Fernet Key value by running the following:

    echo Fernet Key: $(kubectl get secret --namespace airflow airflow-release-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

###########################################################
#  WARNING: You should set a static webserver secret key  #
###########################################################

You are using a dynamically generated webserver secret key, which can lead to
unnecessary restarts of your Airflow components.

Information on how to set a static webserver secret key can be found here:
https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key



