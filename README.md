# InstaPWN
A hackable instagram "clone"

# Getting PWNed

Launch a terminal in the root of this folder, then:

Setup virtualenv and install requirements
```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Create a local sqlite database, apply migrations and run server
```
cd instapwn/
python manage.py migrate
python manage.py runserver
```

Now visit `localhost:8000` and start hacking

To create a superuser do
```
python manage.py createsuperuser
```
and follow the instructions

# Deployments
## Kubernetes
To deploy on kubernetes, only tested on Mac M1/colima

```
brew install colima
colima start -c 4 --kubernetes --kubernetes-ingress
```

Add this line to `/etc/hosts`
```
127.0.0.1 instapwn.loc
```

Deploy the manifest
```
kubectl create namespace instapwn
kubectl apply -f deploy/deployment.yaml
```

This creates a deployment which ensures a pod is running, a service which
exposes the pod's port, and an ingress to expose the service on your local
machine with `instapwn.loc` as the hostname
