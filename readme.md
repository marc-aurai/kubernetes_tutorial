# Introduction 
**This repository is created by Marc Blomvliet (Aurai), which is solely intended for educational purposes.** </br>
</br> 
In this tutorial you will learn how to create an Docker image of your fastAPI application. </br>
The following is included in this application: </br>
* Accepts two questions as input</br>
* Returns a prediction whether the two questions are similar or not similar</br>
* Saves the raw user input data in your MongoDB database </br>
* Predictions are saved in your MongoDB database </br></br>

*The application makes use of my own pre-trained model (with the use of MLFlow). The model is not very accurate but this is not the purpose of this training, neither to bother you with training your own model.* </br>

Furthermore, you will be introduced to MongoDB to create your own FREE database. </br>
Test your Docker image locally with Docker.</br>
Create a Kubernetes cluster with the same Docker image. </br>
The Kubernetes cluster contains the following: </br>
* Deployment </br>
* Load balancer </br>
* Auto scaler (Horizontal Pod Auto scaler)</br>

After you created your Kubernetes cluster, you will perform a stress/load test on your API and therefore on your Kubernetes cluster. </br>

*The pink sections (3.8, 3.9 and 3.10) are optional and just for information.* </br>

Documentation for Python modules is available at: </br>
https://marc-aurai.github.io/kubernetes_tutorial/ </br>


# 1. Create your own MongoDB Database
## 1.1 
Make sure to create your own account on the MongoDB website: </br>
https://account.mongodb.com/account/login?signedOut=true </br>

### 1.1.1
After you created your account and succesfully logged in. </br>
You should add your current IP Address, and afterwards Build a Database. </br>
<img align="left" src="images/mongoDB_step_1.png" width="750"/> <br clear="left"/>

### 1.1.2
Create a Free 'Shared' cluster, and leave it on the default settings. </br>
If you would like, you can add your own cluster name. </br>
<img align="left" src="images/mongoDB_step_2.png" width="750"/> <br clear="left"/> </br>
<img align="left" src="images/mongoDB_step_3.png" width="750"/> <br clear="left"/>

### 1.1.3
After you created your cluster. You are prompted to create a database user. </br>
Create one with a username and password. </br>
<img align="left" src="images/mongoDB_step_4.png" width="750"/> <br clear="left"/>

## 1.1.4 Update the .env 
Update the file with your own credentials. </br>
MONGODB_PASSWORD: Is the password that you created for your database user in step 1.1.3 </br>
MONGODB_SHARED_CLUSTER_NAME: Is the name of your cluster (step 1.1.2), by default it is 'Cluster0'. </br>

# 2. Docker commands

## 2.1 Install Docker
https://docs.docker.com/get-docker/ </br>

## 2.2 Build the docker image </br> (run to make sure your image is working as expected).
> docker build -t <span style="color: orange"> image-name</span> .</br>
> docker run -dp 8020:8020 <span style="color: orange"> image-name</span> </br>

*<span style="color: orange">-image-name-</span> = tutorial-classifier </br>*

***Make sure to be in the root folder API_kubernetes/fastAPI/***  </br>

Go to http://0.0.0.0:8020/docs </br>
<img align="left" src="images/Docker_step_1.png" width="750"/> <br clear="left"/>

And test your API, Click on: POST /predict/  and select '*Try it out*'</br>
Paste two questions inside "*string*", and predict the similarity. </br>
And execute the command. </br>
<img align="left" src="images/fastAPI_step_1.png" width="750"/> <br clear="left"/>

I you got a response, then there should also be data inside your MongoDB Database now. </br>
Go to your MongoDB and click '*Browse Collections*', there should be two tables: Raw_input and Predictions. </br>
<img align="left" src="images/mongoDB_step_5.png" width="750"/> <br clear="left"/> </br>
<img align="left" src="images/mongoDB_step_6.png" width="750"/> <br clear="left"/>

# 3. Kubernetes - Minikube commands
*minikube is local Kubernetes, focusing on making it easy to learn and develop for Kubernetes.* </br>

## 3.1 Install minikube
MacOS with homebrew: 
> brew install minikube </br>

Other OS: </br>
https://minikube.sigs.k8s.io/docs/start/ </br>

## 3.2 Start minikube
> minikube start </br>

## 3.3 Load Docker image to Kubernetes / minikube
> minikube image load <span style="color: orange">-docker image name-</span> </br>

***<span style="color: orange">-docker image name-</span> = tutorial-classifier***

## 3.4 Apply the metrics server, in order to perform auto-scaling
> kubectl -n kube-system apply -f <span style="color: orange">metricserver-0.6.2.yaml</span> </br>

***Make sure to be in the root folder API_kubernetes/kubernetes/***  </br>
</br>

Check if the metric server is working: </br>
> kubectl get pods -n kube-system | grep metrics-server </br>

## 3.5 Deploy with your cluster_config.yml (config file)
> kubectl apply -f <span style="color: orange">cluster_config.yml</span> </br>

***Make sure to be in the root folder API_kubernetes/kubernetes/***  </br>

## 3.6 Get the URL of the Load-balancer service, this is the post.request url to all pods
> minikube service --all </br>

If you add '/docs' to the url of the load-balancer, then you should get the fastAPI page. </br>
Something like: http://127.0.0.1:49700/docs </br> 
The port number will probably be different. </br>

## 3.7 Kubernetes Dashboard UI
> minikube dashboard

<img align="left" src="images/kubernetes_dashboard_1.png" width="750"/> <br clear="left"/>
When your deployment just started, the cluster will use the max amount of pods in order to start-up. </br>
Wait until the cluster is steady with one pod only, before you start the stress/load testing on the cluster (Step 4). </br>

## <span style="color: pink">3.8 Basic commands <span>
> kubectl get pods</br>
> kubectl get deployments</br>
> kubectl get services</br>
> kubectl get hpa </br>

// (Get the horizontal pod autoscalers (HPA))</br>

> kubectl describe svc <span style="color: orange">-service name-</span> </br>

*<span style="color: orange">-service name-</span> = loadbalancer-tutorial </br>*
> kubectl describe deployment <span style="color: orange">-deployment name-</span> </br>

*<span style="color: orange">-deployment name-</span> = tutorial-aurai-classifier </br>*

## <span style="color: pink">3.9 Basic delete commands <span>
> kubectl delete service <span style="color: orange">-service name-</span> </br>

*<span style="color: orange">-service name-</span> = loadbalancer-tutorial </br>*
> kubectl delete deployments <span style="color: orange">-deployment name-</span> </br>

*<span style="color: orange">-deployment name-</span> = tutorial-aurai-classifier </br>*
> kubectl delete hpa <span style="color: orange">-hpa name-</span> </br>

*<span style="color: orange">-hpa name-</span> autoscaler-tutorial </br>*


## <span style="color: pink"> 3.10 Get metrics commands <span>
> kubectl top pods </br>
> kubectl top nodes </br>

# 4. Locust stress testing API
## 4.1 Perfrom the stress/load testing on the Kubernetes cluster/pods
> locust -f <span style="color: orange">./kubernetes/locust_test.py</span> </br>

***Make sure to be in the root folder API_kubernetes***  </br>

The Locust web interface will be started on: http://0.0.0.0:8089 </br>
<img align="left" src="images/locust_web_ui_1.png" width="750"/> <br clear="left"/>
Start with the following settings: </br>
Number of users: 13 </br>
Spawn rate: 1 second </br>
Host: This is the URL from step 3.6 (after you performed: minikube service --all) </br>
Host will probably be something similar like: http://127.0.0.1:49700 </br>
But with a different port number. </br>

Before you start the swarming/load testing, go back to your Kubernetes dashboard: </br>
Workloads -> Pods
<img align="left" src="images/kubernetes_dashboard_2.png" width="750"/> <br clear="left"/>
There is probably only one pod available. </br>

Now start swarming/load testing on the cluster! </br>
Go back to your Kubernetes dashboard, and new pods will pop-up! </br>

Click on one of the pod's name (in **blue**). </br>
<img align="left" src="images/kubernetes_dashboard_3.png" width="750"/> <br clear="left"/>
</br>
Click on '*view logs*' in the right corner, to check whether the certain pod is being used to make predictions. </br>
<img align="left" src="images/kubernetes_dashboard_4.png" width="750"/> <br clear="left"/>
Go through the logs of a couple of pods, to check which pods are being used continuously (set: Auto-refresh -> every 1s). </br>

If you want to stop the load test, go back to your Locust web UI and click '*Stop*'. </br>
Your cluster will take around *~5 minutes* to auto scale down to probably one pod. </br>

If you are interested you can extend the application with your own Snowflake database instead of a MongoDB. </br>
The project is already prepared for this. </br>

*In order to stop the minikube container, perform the following:* </br>
> minikube stop

</br></br>
<style>H1{background:grey;}</style>