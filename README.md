# DGraph+Airflow - Install Guide
This repository contains steps and commands to deploy DGraph and Apache Airflow into K8S

## K8S Cluster on GCP

### Autentication and K8S Cluster Deployment

 - gcloud auth login
 - gcloud config set project tf-my-gcp
 - gcloud container clusters create cluster-dgraph-air --zone us-east1-c --project tf-my-gcp --machine-type e2-standard-2
 - gcloud container clusters get-credentials cluster-dgraph-air --zone us-east1-c --project tf-my-gcp

## DGraph
### Deployment

 - helm repo add dgraph https://charts.dgraph.io  
 - helm install dgraph-release --values dgraph-values.yaml dgraph/dgraph -n dgraph --create-namespace

Customization:

 - helm ls -n dgraph
 - helm show values dgraph/dgraph > dgraph-values.yaml
 - helm upgrade --install dgraph-release dgraph/dgraph -n dgraph -f dgraph-values.yaml --debug

Now, check your deployment:

 - kubectl get pod -n dgraph  
 - kubectl get pvc -n dgraph  
 - kubectl get svc -n dgraph  

#### Option 1: Port-Forward
 - kubectl port-forward service/dgraph-release-dgraph-alpha 8080:8080 -n dgraph  

 - Open: https://play.dgraph.io/?latest#
 - Go to: Dgraph Server Connection  
 - Set Alpha: http://localhost:8080  

 - Check status: http://localhost:8080/state  

#### Option 2: Load-Balancer
 - kubectl get svc -n dgraph  

Get external IPs.
 - Open in your browser Ratel External IP (port 80) > Latest
 - Go to: Dgraph Server Connection  
 - Set Alpha External IP (port 8080)

 - Check status: http://<alphaExternalIP>:8080/state  

### Dgraph Monitoring

 - helm install kube-prometheus-stack --values dgraph_prometheus_v4.yml,dgraph-backup-alert-rules.yml,dgraph-app-alert-rules.yml --set grafana.adminPassword='dgraph-airflow' prometheus-community/kube-prometheus-stack -n dgraph
 - kubectl get pod -n dgraph  
 - kubectl get svc -n dgraph  

Search Grafana External IP: kube-prometheus-stack-grafana and Open in Browser, Ex: 35.222.242.72  
 - Usr: admin  
 - Pwd: dgraph-airflow

## Airflow
### Deployment

 - helm repo add apache-airflow https://airflow.apache.org  
 - helm install airflow-release --values airflow-values.yaml apache-airflow/airflow -n airflow --debug --create-namespace

Customization:

 - helm ls -n dgraph
 - helm show values apache-airflow/airflow > airflow-values.yaml
 - helm upgrade --install airflow-release apache-airflow/airflow -n airflow -f airflow-values.yaml --debug

Now, check your deployment:

 - kubectl get pod -n airflow  
 - kubectl get pvc -n airflow  
 - kubectl get svc -n airflow  

#### Option 1: Port-Forward
 - kubectl port-forward svc/airflow-release-webserver 8081:8080 -n airflow  

 - Open: http://localhost:8081  
 - Usr: admin  
 - Pwd: admin  

#### Option 2: Load-Balancer
 - kubectl get svc -n airflow

Get external IPs.
 - Open in your browser Webserver External IP (port 80)
 - Go to: Dgraph Server Connection  
 - Set Alpha External IP (port 8080)
  

kubectl get pod -n airflow  

### GitSync Repository
 - ssh-keygen -t rsa -C "andysanru@gmail.com"
 - base64 airflow_rsa -w 0 > airflow_rsa.txt
 - Copy gitSshKey to airflow-sync-values.yaml

Fixed know host
 - ssh-keyscan -t rsa github.com > github_public_key
 - ssh-keygen -lf github_public_key

Compare with https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints. If it's right

 - cat github_public_key
 - Copy knownHosts to airflow-sync-values.yaml


> airflow-sync-values.yaml

```yaml
dags:
    gitSync:
        repo: <repo-url>
        branch: main
        depth: 1
        enabled: true
        subPath: dags
        sshKeySecret: airflow-ssh-secret
        knownHosts: |
            github.com ssh-rsa AAAA...1/wsjk=
extraSecrets:
  airflow-ssh-secret:
    data: |
      gitSshKey: '<your-key>'
```

 - helm upgrade --install --values airflow-values.yaml airflow-release apache-airflow/airflow -n airflow -f airflow-sync-values.yaml --debug
 - helm ls -n airflow

## Load Data - DGraph
### Dgraph Live
Copy your RDF files into Alpha Node
 - kubectl cp /home/andres/Documents/work/dk/dgraph-airflow/data/. dgraph-release-dgraph-alpha-0:p/ -n dgraph  

Run dgraph live
 - kubectl exec -it dgraph-release-dgraph-alpha-0 -n dgraph -- dgraph live -f ./data/family.rdf -s ./data/family.schema --format=rdf --zero=dgraph-release-dgraph-zero-0.dgraph-release-dgraph-zero-headless.dgraph.svc.cluster.local:5080 --alpha=localhost:9080 --logtostderr  


```graphql
{  
  movie(func:eq(name, "Homer"))  
  {  
    name  
    parent_to{  
			name  
    }  
  }  
}  
```

Avoid duplicates (upsertPredicate)
 - dgraph live --files /data/1/data/dgraph/sample-data/json/countries1.rdf --alpha localhost:9080 --zero <alphaIP:5080 --format=rdf --upsertPredicate "xid"


### Dgraph Bulk

- kubectl exec -it dgraph-release-dgraph-zero-0 -n dgraph -- sh  

 - apt-get update  
 - apt-get install -y wget file  

 - wget -q -O 1million.schema  "https://github.com/dgraph-io/benchmarks/blob/master/data/1million.schema?raw=true"  
 - wget -q -O 1million.rdf.gz  "https://github.com/dgraph-io/benchmarks/blob/master/data/1million.rdf.gz?raw=true"  


 - dgraph bulk -f 1million.rdf.gz -s 1million.schema --map_shards=1 --reduce_shards=1 --http localhost:8000 --zero=localhost:5080  

 - kubectl cp dgraph-release-dgraph-zero-0:out/. /home/andres/Documents/work/dk/dgraph-airflow/out/ -n dgraph  

Repeat for all Alpha Pods
  - kubectl exec -it dgraph-release-dgraph-alpha-0 -n dgraph -- sh  
  - rm -rf p  
  - mkdir p  
  - chmod 700 p  

Copy files into all Alpha Pods  
 - kubectl cp /home/andres/Documents/work/dk/dgraph-airflow/out/0/p/. dgraph-release-dgraph-alpha-0:p/ -n dgraph  


Restart dgraph server  
  - watch kubectl get pod -n dgraph  
  - kubectl logs -f dgraph-release-dgraph-alpha-0 -n dgraph  

  - http://localhost:8080/admin/shutdown  


Check Schema and Query  (Ratel)

```graphql
{  
  movie(func:alloftext(name@de, "Die schwarz"))  
    @filter(has(genre))  
  {  
    name@de  
    name@en  
    name@it  
  }  
}  
```

### Dgraph Export

 - Method: POST 
 - Endpoint: http://localhost:8080/admin
 - Body:

```
mutation {
  export(input: { format: "rdf" }) {
    response {
      message
      code
    }
  }
}
```


### Airflow Notes  
Default Postgres connection credentials:  
    username: postgres  
    password: postgres  
    port: 5432  


You can get Fernet Key value by running the following:  

    echo Fernet Key: $(kubectl get secret --namespace airflow airflow-release-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)  

###########################################################
###  WARNING: You should set a static webserver secret key  #
###########################################################

You are using a dynamically generated webserver secret key, which can lead to
unnecessary restarts of your Airflow components.  

Information on how to set a static webserver secret key can be found here:  
https://airflow.apache.org/docs/helm-chart/stable/production-guide.html#webserver-secret-key



