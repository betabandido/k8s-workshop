# Kubernetes Workshop (I)

## What is Kubernetes

[Kubernetes in 5 mins](https://www.youtube.com/watch?v=PH-2FfFD2PU)

## Setup the Cluster

Clone https://github.com/betabandido/minikube-provisioner and follow the instructions there to setup a Kubernetes cluster using minikube.

### tmux

You might want to use `tmux` to have multiple virtual terminals multiplexed into a single real one. `Ctrl+B C` creates a new window. `Ctrl+B <number>` switches to the specified window (using its index). `Ctrl+B [` enters scroll mode, and `q` goes back to normal mode.

### Enable Add-ons

```bash
sudo minikube addons enable heapster
sudo minikube addons enable metrics-server
```

## Explore the Cluster

Run the following command to list all the different resources in the cluster:

```bash
kubectl get all --all-namespaces
```

## Creating a Docker Image for the Application

```bash
cd ~/k8s-workshop/hello
sudo docker build -t hello:0.1 .
```

## Creating a Deployment

Deploy the application on Kubernetes:

```bash
kubectl apply -f k8s/deployment.yaml
```

List the deployments and pods:

```bash
kubectl get deployments
kubectl get pods
```

Display some more information:

```bash
kubectl describe deployment hello
kubectl describe pod hello
```

Show the application logs:

```bash
kubectl logs -l app=hello

# It is also possible to get the logs for a particular pod, given its name:
kubectl logs <pod-name>
```

Connecting to a pod:

```bash
kubectl exec <pod-name> -it -- sh
```

## Updating a Deployment

Update `k8s/deployment.yaml` so that the deployment uses two replicas:

```yaml
# ...
spec:
  # ...
  replicas: 2
  # ...
```

And then apply the configuration again:

```bash
kubectl apply -f k8s/deployment.yaml
```

Listing the pods must now show two pods for application `hello`:

```bash
kubectl get pods -l app=hello
```

## Creating a Service

```bash
kubectl apply -f k8s/service.yaml
```

List the services in the cluster:

```bash
kubectl get services
```

Find some more information about the created service:

```bash
kubectl describe service hello
```

In a traditional Kubernetes cluster the external IP would be shown. In Minikube, however, the external IP must be obtained by running:

```bash
minikube service hello --url
```

Use `curl` to verify you can access the application:

```bash
curl $(minikube service hello --url)
```

Use the external address of the EC2 instance (not the one for the service) to access the application from your browser: `http://ec2-<external-IP>.eu-west-1.compute.amazonaws.com:<port>`

## Dashboard

Get the dashboard's port running the following command:

```bash
minikube dashboard --url
```

Then use that port together with the external address of the EC2 instance to access the dashboard.

Explore the different resources in the cluster (pods, deployments, services, etc.).

## Updating a Deployment

Change `main.py` so that it returns another message, and then create a new docker image with a new tag:

```bash
sudo docker build -t hello:0.2 .
```

Now, update `deployment.yaml` so that it uses image `hello:0.2`. After that, update the deployment using:

```bash
kubectl apply -f k8s/deployment.yaml
```

Use your browser to check whether the message has changed.

## Dealing with Deployment Failures

Change `main.py` so that the `healthz` endpoint returns an error:

```python
from flask import Flask, abort

# ...

@app.route('/healthz')
def healthz():
    abort(500)
```

Create a new docker image:

```bash
sudo docker build -t hello:0.3 .
```

Update the `deployment.yaml` file to use the new image, and update the deployment:

```bash
kubectl apply -f k8s/deployment.yaml
```

Watch pod status:

```bash
watch kubectl get pods
```

To rollback the deployment execute:

```bash
kubectl rollout undo deployment/hello
```

## Autoscaling

Create and deploy the `cpu` application (this application performs a CPU-intensive operation when it receives a request):

```bash
cd ~/k8s-workshop/cpu
sudo docker build -t cpu:0.1 .
kubectl apply -f k8s
```

### Performance Monitoring

Run the following command to send traffic to the application:

```bash
while true; do curl $(minikube service cpu --url) ; done
```

After some seconds you should see an increase in CPU utilization. Then, the auto-scale mechanism will trigger, creating new replicas. Run the following command to see the new replicas being created:

```bash
watch kubectl get pods
```

## Next Steps

To create a full-fledged Kubernetes cluster have a look at [kops](https://github.com/kubernetes/kops).
