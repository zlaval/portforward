# Port forward

---
Forwards the data stream from the remote service to `localhost:5000`

## Properties:

**CONNECT_HOST**: remote service address  
**CONNECT_PORT**: port of the remote service

### Example
Forwars RDS Postgres from the VPC into the pod's localhost then use kubectl port-forward for reaching it on your local machine.

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portforward
spec:
  replicas: 1
  selector:
    matchLabels:
      app: portforward
  template:
    metadata:
      labels:
        app: portforward
    spec:
      containers:
        - name: portforward
          image: zalerix/forwardstream:1.0.0
          envFrom:
            - configMapRef:
                name: portforward-config
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: portforward-config
data:
  CONNECT_HOST: '<mydatabaseurl.com>'
  CONNECT_PORT: '5432'
```

The port forward command:
```kubectl port-forward <portforward pod's name> 5000:5000```

The database is available on `localhost:5000`


[DockerHub Image](https://hub.docker.com/r/zalerix/forwardstream)