# Comandos básicos de debugging dentro del cluster

- `kubectl logs <pod_name>`

Este comando se utiliza en Kubernetes para ver los registros (logs) generados por los contenedores en un pod específico.

- `kubectl get <resource> -o wide`

Este comando se utiliza para obtener información sobre los recursos de Kubernetes. La sintaxis `<resource>` se reemplaza con el tipo de recurso que deseas obtener, como pods, servicios, despliegues, etc. El modificador `-o wide` se utiliza para mostrar una salida más detallada y amplia que incluye información adicional, como las direcciones IP, los nodos en los que se ejecutan los recursos, etc. Es útil para obtener una visión más completa de los recursos y su estado en el clúster de Kubernetes.

- `kubectl describe <resource> <id/name>`

Al ejecutar este comando, obtendrás información detallada sobre el recurso, incluidos los eventos relacionados con él, su estado actual, las etiquetas asociadas, etc.

- `kubectl run -i --rm --tty debug --image=busybox --restart=Never -- sh`

Este comando ejecuta un pod en forma interactiva usando una image de busybox. Al finalizar la ejecución el Pod es destruido.
Parados el pod podemos alcanzar la IP y puertos de cualquier Pod corriendo.

# Recursos básicos
Primero vamos a subir la guía al host master si es que todavía no la tienen en el host master. Desde este directorio corremos:
```bash
scp * <ubuntu@your_master_ec2>:~
```

Ahora vamos a abrir **dos** terminales en el nodo master.

Una terminal la vamos a utilizar para observar los cambios. Corremos el siguiente comando para observar en vivo los cambios en la lista de pods:
```bash
watch kubectl get pods -o wide
```

En la segunda terminal corremos todos los comandos que vamos a ir mencionando a continuación.

## Pod

El archivo `simple-pod.yaml` define un pod con la imagen de nginx:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:1.14.2
      ports:
        - containerPort: 80
```

Para levantarlo corremos:

```bash
kubectl apply -f simple-pod.yaml
```

y en la otra terminal vemos:

```bash
NAME    READY   STATUS    RESTARTS   AGE   IP              NODE     NOMINATED NODE   READINESS GATES
nginx   1/1     Running   0          7s    192.168.247.1   node-2   <none>           <none>
```

Podemos observar el estado del pod, el nodo donde está corriendo, su IP, entre otras cosas.

Le podemos pegar al nginx y ver que existe con:
```bash
curl $(kubectl get pod nginx --template={{.status.podIP}})
```

También podemos ver una descripción de la configuración del pod con:

```bash
kubectl get pods nginx -o yaml
```

```bash
kubectl describe pods nginx
```

Además, podemos correr comandos dentro del nodo como por ejemplo para ver el estado de nginx con:

```bash
kubectl exec -it nginx -- service nginx status
```

También podemos entrar al pod con:

```bash
kubectl exec --stdin --tty nginx -- /bin/bash
```

Podemos cambiar la configuración, ver las diferencias y aplicarlas. Por ejemplo, si cambiamos la versión de nginx:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx:1.14.1
      ports:
        - containerPort: 80
```

El siguiente comando nos muestra las diferencias:

```bash
kubectl diff -f simple-pod.yaml
```

Si corremos el apply, va a configurar el pod a la nueva versión y en el watch nos va a aparecer que tiene un RESTART el pod. 
```bash
kubectl apply -f simple-pod.yaml
```
Por último, lo eliminamos con:

```bash
kubectl delete pods nginx
```

## Replica set

Un ReplicaSet en Kubernetes es un objeto que permite garantizar la disponibilidad y la escalabilidad de las aplicaciones en un clúster. Es una abstracción que define un conjunto de réplicas de un Pod (unidad mínima en Kubernetes) y asegura que siempre haya una cantidad específica de réplicas en funcionamiento.

El ReplicaSet monitorea constantemente el estado de las réplicas y, en caso de que alguna de ellas falle o sea eliminada, se encarga de crear automáticamente nuevas réplicas para reemplazarlas. Esto garantiza que la aplicación siga funcionando correctamente incluso en situaciones de fallas o interrupciones.

Además, el ReplicaSet permite escalar vertical u horizontalmente la cantidad de réplicas de un Pod. Esto significa que se puede aumentar o disminuir la cantidad de réplicas en función de la carga de trabajo o los recursos disponibles, lo que permite adaptar la capacidad de la aplicación a las necesidades cambiantes.

El archivo simple-rs.yaml define un replica set simple:

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: web
  labels:
    env: dev
    role: web
spec:
  replicas: 4
  selector:
    matchLabels:
      role: web
  template:
    metadata:
      labels:
        role: web
    spec:
      containers:
        - name: testnginx
          image: nginx
```

Lo creamos:

```bash
kubectl apply -f simple-rs.yaml
```

Para ver su estado utilizamos:

```bash
kubectl get rs -o wide
```

y obtenemos:

```bash
NAME   DESIRED   CURRENT   READY   AGE   CONTAINERS   IMAGES   SELECTOR
web    3         3         3       37s   testnginx    nginx    role=web
```

Luego, observamos los pods creados:

```bash
NAME        READY   STATUS    RESTARTS   AGE   IP               NODE     NOMINATED NODE   READINESS GATES
web-gsp9s   1/1     Running   0          54s   192.168.84.135   node-1   <none>           <none>
web-nz4p7   1/1     Running   0          54s   192.168.247.6    node-2   <none>           <none>
web-slwxj   1/1     Running   0          54s   192.168.247.5    node-2   <none>           <none>
```

Podemos ver que se distribuyeron los pods en distintos nodos.

El RS adopta los nodos según el criterio que definimos en el yaml previamente:

```yaml
selector:
  matchLabels:
    role: web
```

**Siempre se asegura que tengamos la cantidad de pods deseada.**

Para probarlo:

- Observen la cantidad de pods antes y después de eliminar un pod con (Al eliminarlo, el rs crea otro):

```bash
kubectl delete pods <nombre_de_uno_de_los_pods>
```

- Levanten un nuevo pod con la misma label que usa el replica set
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: orphan
  labels:
    role: web
spec:
  containers:
    - name: orphan
      image: httpd
```
```bash
kubectl apply -f orphan-pod.yaml
```
Al aplicar el pod podemos ver que automáticamente es borrado por el replica set, ya que al ver que tiene ya la cantidad de pods deseada, aquellos que coinciden con el selector, son considerados innecesarios, y se eliminan.

En cambio, si invertimos el orden de ejecución y el pod estuviera corriendo antes de iniciar el replica set, el pod es adoptado y agregado a la lista de los pods controlados por el replica set.

> [!NOTE]
> El destino de los pods adoptados pasa a ser el mismo del ReplicaSet. Si borro el ResplicaSet, todos los recursos gestionados serán borrados.

En caso de querer borrar el ReplicaSet, pero no los pods, se puede usar la opción `--cascade=orphan`, que le da independencia a los pods, que luego debe ser borrados en forma independiente.

Para eliminar el rs:
```bash
kubectl delete rs web
```

En resumen, un ReplicaSet en Kubernetes es un componente esencial para garantizar la disponibilidad, la tolerancia a fallos y la escalabilidad de las aplicaciones en un clúster, al mantener un conjunto de réplicas de los Pods y gestionar su estado de manera automática.

## Deployments

Un deployment en Kubernetes es un componente fundamental que permite administrar y controlar la ejecución de aplicaciones dentro de un clúster de Kubernetes. En pocas palabras, se refiere al proceso de despliegue y gestión de aplicaciones en contenedores en un entorno de Kubernetes.

En un deployment, se define una especificación que describe cómo debe ser ejecutada la aplicación en el clúster. Esta especificación incluye detalles sobre la imagen del contenedor, la cantidad de réplicas que se deben crear, los recursos que se asignarán a cada réplica y otras configuraciones relacionadas.

Cuando se crea un deployment, Kubernetes se encarga de crear y gestionar los recursos necesarios para ejecutar la aplicación. Esto implica la creación de réplicas del contenedor, la asignación de recursos, la distribución de carga, la supervisión de la salud de las réplicas y la implementación de actualizaciones de manera controlada.

Una vez que se ha creado un deployment, Kubernetes garantiza que la cantidad especificada de réplicas esté siempre en funcionamiento. En caso de que una réplica falle o se deteriore, Kubernetes automáticamente creará una nueva réplica para reemplazarla y mantener la disponibilidad de la aplicación.

> [!NOTE]
> Un ReplicaSet garantiza que un número específico de réplicas de un pod se está ejecutando en todo momento. Sin embargo, un Deployment es un concepto de más alto nivel que gestiona ReplicaSets y proporciona actualizaciones de forma declarativa de los Pods junto con muchas otras características útiles. Por lo tanto, se recomienda el uso de Deployments en vez del uso directo de ReplicaSets, a no ser que se necesite una orquestración personalizada de actualización o no se necesite las actualizaciones en absoluto.

Vamos a definir un deployment en el archivo `simple-deployment.yaml`:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
```
Si lo aplicamos:
```bash
kubectl apply -f simple-deployment.yaml
```
Vamos a poder ver que se creo un replica set con sus respectivos pods.

**La ventaja del Deployment sobre el ReplicaSet es la capacidad de hacer cambios en el despligue de la aplicación sin afectar el servicio.** 

Por ejemplo: podemos actualizar la versión de de la imagen del Deployment y en forma prograsiva se irá actualizando cada uno de los pods.

```bash
kubectl set image  deploy/nginx nginx=nginx:1.24.0
```
Si observamos en la otra terminal, se matan los pods a medida que tiene uno nuevo con la nueva versión corriendo:
```
NAME                     READY   STATUS              RESTARTS   AGE
nginx-595dff4799-hwr66   0/1     ContainerCreating   0          0s
nginx-595dff4799-nflm2   1/1     Running             0          3s
nginx-595dff4799-tjp6n   1/1     Running             0          1s
nginx-86dcfdf4c6-kstzm   1/1     Running             0          44s
nginx-86dcfdf4c6-psdnd   0/1     Terminating         0          43s
```

Si los pods no se levantan, no se van a eliminar los pods anteriores:
```bash
kubectl set image  deploy/nginx nginx=nginx:9.9.9
```
```bash
NAME                     READY   STATUS             RESTARTS   AGE
nginx-595dff4799-hwr66   1/1     Running            0          4m25s
nginx-595dff4799-nflm2   1/1     Running            0          4m28s
nginx-595dff4799-tjp6n   1/1     Running            0          4m26s
nginx-8f7bcb6d7-m86hn    0/1     ImagePullBackOff   0          28s
```

Al hacer un cambio no deseado o que detectamos que no está funcionando correctamente, podemos hacer facilmente rollback. Por ejemplo, para retraer el cambio de la versión erroneo utilizamos:

```bash
kubectl rollout undo deployments/nginx
```
```
NAME                     READY   STATUS    RESTARTS   AGE
nginx-595dff4799-hwr66   1/1     Running   0          7m23s
nginx-595dff4799-nflm2   1/1     Running   0          7m26s
nginx-595dff4799-tjp6n   1/1     Running   0          7m24s
```

El ReplicaSet creado después de la modificación hecha en el deployment, fue destruido y se conservó el deployment original.

Para eliminar el deployment:
```bash
kubectl delete deployment nginx
```

En resumen, un deployment en Kubernetes permite desplegar y gestionar aplicaciones en contenedores de manera eficiente, asegurando la escalabilidad, la alta disponibilidad y la gestión de recursos en un clúster de Kubernetes.

## DeamonSet

Un DaemonSet en Kubernetes es un tipo de controlador que garantiza que un pod se ejecute en todos los nodos disponibles en un clúster. A diferencia de otros controladores de replicación, como los ReplicationSets, que pueden crear y administrar múltiples instancias de un pod, un DaemonSet asegura que exactamente una instancia de un pod esté presente en cada nodo del clúster.

Cada vez que se agrega un nuevo nodo al clúster o se detecta la eliminación de un nodo, el DaemonSet automáticamente crea o destruye un pod en el nodo correspondiente. Esto garantiza que el pod esté en funcionamiento en todos los nodos y se ajuste al tamaño del clúster sin necesidad de intervención manual.

Los DaemonSets son útiles para implementar agentes de monitoreo, registradores de registros o servicios de red que necesitan ejecutarse en todos los nodos del clúster. Además, pueden utilizarse para tareas de administración del sistema, como recolectar métricas o realizar actualizaciones en todos los nodos.

Creamos el archivo `simple-daemonset.yaml`:
``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: logger
  labels:
    app: logger
spec:
  selector:
    matchLabels:
      name: logger
  template:
    metadata:
      labels:
        name: logger
    spec:
      containers:
      - name: logger
        image: busybox
        command: ["sleep","infinity"]
        volumeMounts:
        - name: varlog
          mountPath: /var/log
      volumes:
      - name: varlog
        hostPath:
          path: /var/log
```

Desplegamos:

```bash
kubectl apply -f simple-daemonset.yaml
```
```bash
kubectl get daemonset
```
Vemos en la otra terminal que hay uno desplegado por nodo:
```
NAME           READY   STATUS    RESTARTS   AGE    IP               NODE     NOMINATED NODE   READINESS G
ATES
logger-9sflh   1/1     Running   0          2m5s   192.168.84.141   node-1   <none>           <none>
logger-qxjdj   1/1     Running   0          2m5s   192.168.247.10   node-2   <none>           <none>
```

Ahora podemos saltar dentro del pod y ver los logs del nodo.

```bash
kubectl exec -it <nombre_de_uno_de_los_pods> -- ls -R /var/log/pods/
```

En resumen, un DaemonSet en Kubernetes es un controlador que garantiza la presencia de un pod en todos los nodos del clúster, lo que permite ejecutar tareas específicas en cada uno de ellos de manera automatizada.

Para eliminarlo:
```bash
kubectl delete daemonset logger
```

## Storage


Un PersistentVolume (PV) en Kubernetes es un recurso que proporciona almacenamiento persistente en un clúster de Kubernetes. Es una abstracción que representa un volumen físico o un recurso de almacenamiento en la infraestructura subyacente, como un disco duro en un servidor o un volumen de red.

Un PersistentVolume se define por su capacidad de almacenamiento, acceso y modo de reclamación. La capacidad de almacenamiento indica la cantidad de datos que se pueden almacenar en el volumen. El acceso se refiere a cómo los pods pueden acceder al volumen, ya sea de forma exclusiva (acceso de lectura-escritura) o compartida (acceso de solo lectura). El modo de reclamación define cómo se asigna y libera el volumen.

Los PersistentVolumes se crean de forma independiente de los pods y los nombres de los volúmenes no están directamente vinculados a ningún pod en particular. En su lugar, los pods pueden reclamar y utilizar los PersistentVolumes mediante PersistentVolumeClaims (PVC). Un PVC especifica los requisitos de almacenamiento que necesita un pod y solicita un PersistentVolume compatible que cumpla con esos requisitos.

Para esta parte hay que crear una carpeta en ambos workers:
``` bash
ssh ubuntu@<reemplazar_para_el_nodo_1> 'mkdir -p /tmp/cluster/pv1'
ssh ubuntu@<reemplazar_para_el_nodo_2> 'mkdir -p /tmp/cluster/pv1'
```

Vamos a levantar dos persistent volumes. Cada uno tiene afinidad a un worker distinto, por lo que se van a crear uno en cada worker. Por ejemplo, para el nodo 1:
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: cluster-pv
spec:
  capacity:
    storage: 1Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Delete
  storageClassName: local-storage
  local:
    path: /tmp/cluster/pv1
  nodeAffinity:
    required:
      nodeSelectorTerms:
        - matchExpressions:
            - key: kubernetes.io/hostname
              operator: In
              values:
                - node-1
```
Notemos que estamos declarando un `nodeAffinity` al `node-1` por lo que se va a levantar solo en ese nodo. Además, `persistentVolumeReclaimPolicy: Delete` hace que se borre el pv cuando se borra el persistent volume claim, es decir, cuando se deja de usar se borra solo. 

Los aplicamos:

``` bash
kubectl apply -f simple-pv-1.yaml
kubectl apply -f simple-pv-2.yaml
```
Vemos que se levantaron:
```bash
kubectl get pv
```
```bash
NAME           CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS    VOLUMEATTRIBUTESCLASS   REASON   AGE
cluster-pv-1     1Gi        RWO            Delete           Available           local-storage   <unset>                          46s
cluster-pv-2   1Gi        RWO            Delete           Available           local-storage   <unset>                          6s
```
Cuando un PersistentVolumeClaim se realiza, Kubernetes encuentra un PersistentVolume disponible que cumpla con los requisitos y lo enlaza al PVC. A continuación, el PVC se puede montar en los pods que lo soliciten, proporcionándoles almacenamiento persistente. Esto permite que los datos se conserven incluso si los pods se eliminan o reinician.

Vamos a levantar el archivo `stateful.yaml` que crea un StatefulSet:
```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: "nginx"
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
          name: web
        volumeMounts:
        - name: www
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: www
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: local-storage
      resources:
        requests:
          storage: 1Gi
```

Aplicando este último archivo:

``` bash
kubectl apply -f stateful.yaml
```
```
NAME    READY   STATUS    RESTARTS   AGE     IP               NODE     NOM
INATED NODE   READINESS GATES
web-0   1/1     Running   0          4m23s   192.168.84.143   node-1   <no
ne>           <none>
web-1   1/1     Running   0          4m21s   192.168.247.11   node-2   <no
ne>           <none>
web-2   0/1     Pending   0          4m19s   <none>           <none>   <no
ne>           <none>
```
Y con:
```bash
kubectl get pvc
```
```
NAME        STATUS    VOLUME         CAPACITY   ACCESS MODES   STORAGECLASS    VOLUMEATTRIBUTESCLASS   AGE
www-web-0   Bound     cluster-pv-1     1Gi        RWO            local-storage   <unset>                 4m49s
www-web-1   Bound     cluster-pv-2   1Gi        RWO            local-storage   <unset>                 4m47s
www-web-2   Pending                                            local-storage   <unset>                 4m45s
```
Se puede ver que dos de los PVC lograron hacer binding con los PV de cada nodo, pero el otro no encontró candidato, por lo tanto, el pod no puede ser creado, ya que su dependencia no está disponible.

Para eliminar los pv, basta con eliminar los pvc.
