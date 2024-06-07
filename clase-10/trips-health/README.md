# Implementando Health checks en Trips
## Paso 1

Agregar un endpoint que responsa si el servicio está vivo en cada uno de los componentes

```python
from nameko.web.handlers import http

class GatewayService:
    ...

    # Dentro del componente 
    @http('GET', '/health')
    def health_check(self, request):
        return 200 , "Up and running"
```

Confirmar que está operativo ejecutando desde la máquina host:

```bash
docker compose up -d --build  
## Verifico gateways
curl localhost:8000/health
## Verifico trips desde gateways
docker exec -ti trips-health-gateway-1 curl trips:8000/health
## Verifico airports desde gateways
docker exec -ti trips-health-gateway-1 curl airports:8000/health
```

Con esto tenemos una manera de verificar si el servicio está funcionando y teniendo un balanceador adelante, el balanceado puede determinar si el grupo de servicios de trips está andando. Si falla al acceder al puerto 8000, o si el acceso al `http://gateways:8000/health` no responde `200`, el servicio está caído.

# Paso 2

En gateways necesitamos que los otros servicios estén OK para funcionar, entoncs vamos a evaluarlo. Para eso vamos a crear un servicio genéricos que podamos ir extendiendo:

Agregamos una inicialización de las clases según corresponda
```python
HEALTH_CHECK_PERIOD = 60 # in seconds

class GatewayService:

    def __init__(self):
        self.health_check_func = {}
        self.health_check_time = int( time.time() )

```


Reescribimos el health check
```python
    @http('GET', '/health')
    def health_check(self, request):
        now = int(time.time())
        healthy = True
        message = []
        if (now - self.health_check_time) > HEALTH_CHECK_PERIOD:
            for k,check in self.health_check_func.items():
                func_status_ok , func_message = check(self)
                message.append( f'{k} status: {"OK" if func_status_ok else "Error. "+func_message}' )
                healthy &= func_status_ok
            self.health_check_time = now

        message.insert(0, f"{self.name} status: {'OK' if healthy else 'Error'}\nDependencies:")

        return (200 if healthy else 500 ) , '\n'.join(message)
```

Recreamos y volvemos a probar:
```bash
docker compose up -d --build  
## Verifico gateways
curl localhost:8000/health
## Verifico trips desde gateways
docker exec -ti trips-health-gateway-1 curl trips:8000/health
## Verifico airports desde gateways
docker exec -ti trips-health-gateway-1 curl airports:8000/health
```

Vamos a comenzar a diseñar testeos 