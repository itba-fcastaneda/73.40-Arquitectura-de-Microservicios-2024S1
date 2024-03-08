# Docker Compose

Docker compose es una herramienta que permite orquestar la ejecución de multiples contenedores de forma declarativa. Para ello se Utiliza un archivo YAML donde se declaran los servicios (contenedores), redes, volúmenes, secretos, etc. que se desean utilizar junto con sus interdependencias. Luego, al ejecutar la herramienta se crearán los recursos en el orden correspondiente para cumplir con los requisitos.

Toda la funcionalidad y configuraciones utilizadas desde compose son nativas de Docker. Compose simplemente ofrece una forma mas cómoda y organizada de utilizarlas.

## Introducción

Docker compose está compuesto por una herramienta dentro del paquete docker `docker compose` y un archivo (usualmente llamado) `docker-compose.yaml`.

El archivo YAML contiene la declaración de los distintos recursos necesarios para ejecutar nuestra aplicación. Estos incluyen contenedores, redes, volúmenes, y secretos. Además, el archivo declara la versión de "compose file" que se está utilizando.

> **Sobre las versiones**
>
> Si buscan sobre la versión de compose verán que hay 2 tipos de versiones. Existe la versión de la herramienta en sí y la versión del archivo. Si bien esta relacionada, la versión del archivo tiene que ver con la funcionalidad permitida mientras que la versión de la herramienta esta vinculada a la implementación de la misma.
>
> La diferencia con las versiones de la herramienta son el uso de `docker-compose` (v1) y `docker compose` (v2). Lo recomendado es utilizar la v2, si en algún momento se encuentran un comando con el guión medio deberían cambiarlo por la versión más moderna.
>
> En el caso de la versión del archivo, es importante tenerla en cuenta a la hora de configurar nuestros recursos. En la documentación verán que algunas funcionalidad están a partir de X versión. Recomendable utilizar la ultima disponible (`3.8` al día de escritura)

Salvando el caso especial de la versión, el archivo está compuesto por entradas asociadas a cada tipo de recurso. Dentro de las mismas se declaran todas las instancias de esos recursos.

```yaml
version: '3.8'

services:
    db:
        ...
    wordpress:
        ...

secrets:
    db_password:
        ...
    db_root_password:
        ... 

volumes:
    db_data:
        ...
networks:
    db_network:
        ...
```

En este ejemplo se puede ver que se declararon 2 contenedores (services), 2 secretos, 1 red y 1 volumen.

## Contenedores, redes y volúmenes

A modo de ejemplo voy a construir un docker compose para levantar Prometheus. Una base de datos para métricas. Hay que tener en cuenta que la misma almacena información la cual queremos que persista y expone sus datos vía HTTP por el puerto 9090.

Si bien pueden encontrar los archivos en su estado final en la carpeta de example-code, los invito a seguir el paso a paso para entender bien cada concepto.

### Servicio

Los servicios son la parte principal del compose, es donde declaramos los containers.

El único requisito necesario a la hora de levantar un contenedor es especificar que imagen utilizar. Para ello tenemos dos opciones.

Por un lado tenemos la opción de `image` la cual funciona igual que cuando se utiliza docker desde la CLI. Lo principal es declarar el nombre de la misma. Además se puede especificar el tag y el registry donde esta almacenada. Estos valores toman como default `latest` y DockerHub respectivamente. Es recomendable fijar el tag en función de la versión que estemos utilizando. En el caso del registry será necesario declararlo cuando utilicemos una imagen proveniente de otro que no sea el default.

La otra opción es utilizar la opción de `build`. En este caso la imagen a utilizar todavía no existe y vamos a decirle a docker compose como hacer para construirla. Veremos más adelante que implica construir una imagen.

El primer paso, como fue mencionado es definir la imagen a utilizar. En este caso se eligió dentro de `prom/prometheus` la versión `v2.46.0`

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
```

Una vez definido lo esencial, podemos agregar el resto de configuraciones.

- Vamos a forwardear el puerto 9090 para que pueda ser accedido desde el host
- Vamos a definir un nombre al container para poder identificarlo mejor: `backend_prom`
- Vamos a especificar una [política de restart](https://docs.docker.com/config/containers/start-containers-automatically/#use-a-restart-policy)

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
        container_name: backend_prom
        ports:
        - 9090:9090
        restart: unless-stopped
```

Luego agregaremos una aplicación de ejemplo que alimente la base de datos. En este caso será `isagues/dummy_exporter:1.0`

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
        container_name: backend_prom
        ports:
        - 9090:9090
        restart: unless-stopped
    
    app:
        image: isagues/dummy_exporter:1.0
```

### Red

Estas dos aplicaciones queremos que se comuniquen utilizando una red exclusiva entre ellas. Vamos a declarar una nueva red y asignarla a los 2 servicios. Haremos que la misma sea internal para que no haya salida a internet.

> **Redes internal**
>
> Las redes internas no tienen definido un gateway que les permita salir de la red en cuestión. Como consecuencia, si se realiza un forward de puerto a un contenedor cuya única red es internal, el mismo no funcionará como es esperado. Para solucionar este inconveniente es necesario declarar por lo menos una red externa. Ademas de la(s) redes internas a las cuales pertenezca el contenedor en cuestión.

Teniendo en cuenta esta salvedad, agregaremos una segunda red NO interna para que el contenedor pueda ser accedido.

> **Este ejemplo va en contra de todos los ejemplos tradicionales donde la DB es lo que esta escondido y la aplicación pública** (es para que después tengan que pensar como resolver el caso más general :D)

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
        container_name: backend_prom
        ports:
        - 9090:9090
        restart: unless-stopped
        networks:
        - dummy
        - dmz
    
    dummy_app:
        image: isagues/dummy_exporter:1.0
        networks:
        - dummy

networks:
    dummy:
        name: backend_network_dummy
        internal: true
    dmz:
        name: backend_network_dmz
```

### Persistencia

Luego, como Prometheus es una DB queremos que la información la cual persista más allá del ciclo de vida del container. Para ello agregaremos un volumen. En este caso como queremos dar persistencia y no montar archivos externos vamos a usar un volumen de docker. 

Para estos casos es importante saber dónde persiste la información la aplicación. Las imágenes mejor documentadas lo detallan en su descripción, en el caso de esta imagen no es evidente. [Explorando un poco](https://github.com/prometheus/prometheus/blob/main/Dockerfile) podemos encontrar que la data esta ubicada en `/prometheus`.

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
        container_name: backend_prom
        ports:
        - 9090:9090
        restart: unless-stopped
        volumes:
        - prom_data:/prometheus
        networks:
        - dummy
        - dmz
    
    dummy_app:
        image: isagues/dummy_exporter:1.0
        container_name: backend_dummy
        networks:
        - dummy

networks:
    dummy:
        name: backend_network_dummy
        internal: true
    dmz:
        name: backend_network_dmz

volumes:
  prom_data:
```

Por último, vamos a agregar el archivo de configuración para Prometheus. Este va a estar en el mismo directorio que el archivo `docker-compose.yaml` bajo el nombre de `prometheus.yaml`. Tendrá el siguiente contenido:

```yaml
global:
  scrape_interval: 15s
  scrape_timeout: 10s
  evaluation_interval: 15s

scrape_configs:
- job_name: dummy
  honor_timestamps: true
  metrics_path: /metrics
  static_configs:
  - targets:
    - dummy_app:8080
```

Al igual que el directorio de persistencia, es importante saber donde levanta la configuración la imagen que vamos a utilizar. En este caso seria en `/etc/prometheus/`. Por lo tanto, vamos a montar el archivo generado en esa dirección. Dado que es un archivo de configuración y no tenemos ninguna intención de que sea modificado por la aplicación, podemos especificar que el mismo es read only (ro).

```yaml
version: '3.8'

services:
    prometheus:
        image: prom/prometheus:v2.46.0    
        container_name: backend_prom
        ports:
        - 9090:9090
        restart: unless-stopped
        volumes:
        - prom_data:/prometheus
        - ./prometheus.yaml:/etc/prometheus/prometheus.yml:ro
        networks:
        - dummy
        - dmz
    
    dummy_app:
        image: isagues/dummy_exporter:1.0
        container_name: backend_dummy
        networks:
        - dummy

networks:
    dummy:
        name: backend_network_dummy
        internal: true
    dmz:
        name: backend_network_dmz

volumes:
  prom_data:
```

### Levantar los servicios

Una vez definidos todos estos archivos podemos verificar el funcionamiento ejecutando `docker compose up -d` en el directorio con los dos archivos. Como consecuencia se generarán todos los servicios declarados. Podemos ver que se generaron:

- Las redes: `docker network ls | grep -E 'dmz|dummy'`
- Los containers: `docker container ls | grep -E 'prom|dummy'`
- El volumen: `docker volume ls | grep 'prom_data'`

Por otro lado, podemos verificar que este corriendo de forma esperada accediendo desde el navegador al puerto 9090 de donde este corriendo docker. Yendo a `Status > Targets` en la barra de navegación deberían encontrarse con una lista que contiene a dummy. Después de unos segundos de iniciar ambos servicios el estado de dummy debería pasar de `UNKNOWN` a `UP`. Esto significa que el sistema está funcionando y Prometheus puede acceder a dummy.

> **A resolver**
>
> Si bien no es problemático que por un tiempo Prometheus no se pueda comunicar con la aplicación, estaría bueno que primero levante dummy y cuando este listo levante Prometheus. Investigar como resolver esta "condición de carrera"
> <details>
> <summary>Pista</summary>
>
> Investigar `healthcheck` y `depends_on`
> </details>

Para finalizar la ejecución basta con ejecutar `docker compose down`.
## Variables de ambiente y secretos

Un aspecto importante a tener en cuenta a la hora de utilizar herramientas como Docker compose son los secretos y valores dependientes del entorno. Estos son valores que no conviene tener hardcodeados en nuestro código. Por un lado los secretos no deberían estar versionados con el mismo nivel de visibilidad que el compose. Estos deberían ser gestionado en formas seguras y por menos personas. En el caso de los valores dependientes del entorno, estos conviene que este separados para darle flexibilidad al código. Es preferible escribir una única configuración y solo adaptar los valores necesarios para cada caso.

### Variables de ambiente

Valores almacenados por el sistema disponibles para los procesos. Son útiles para configurar los servicios en runtime. 

La forma mas simple de utilizarlas consiste en asignarlas de forma directa al contenedor. Son provistas en forma de clave valor, luego serán cargadas en el ambiente del proceso generado y podrán ser consultadas como cualquier variable de entorno.

```yaml
version: '3.8'

services:
    db:
        image: postgres:15.4
        environment:
        - POSTGRES_DB=airports
```

En este caso estamos definiendo el nombre de la DB a generar en el motor Postgres sea `airports`. Si bien la imagen es reutilizada, nuestro `docker-compose.yaml` queda fijo al nombre `airports`. Si quisiésemos usar el mismo compose con otro servicio esta solución no seria lo suficientemente flexible. Para abordar este inconveniente tenemos dos opciones.

Por un lado podemos utilizar las variables de ambientes disponibles en el proceso que esta ejecutando el comando `docker compose` en el host.

```yaml
version: '3.8'

services:
    db:
        image: postgres:15.4
        environment:
        - POSTGRES_DB=${DB_NAME}
```

Otra opción es utilizando un archivo que contenga todos los valores a ser definidos.

passengers_db.env
```.env
POSTGRES_DB=passengers
```

```yaml
version: '3.8'

services:
    db:
        image: postgres:15.4
        env_file:
        - passengers.env
```

La ventaja de esta opción es que no solo desacoplamos los valores a ser asignado sino cuales son los valores que pueden ser definidos. Dotando de mayor flexibilidad al `docker-compose.yaml`

> **Mas opciones**
>
> Hay varias formas de definir variables de entorno para ser interpretadas dentro de compose. Para mayor detalle sobre como toman presidencia pueden encontrarlo en la [documentación de compose](https://docs.docker.com/compose/environment-variables/envvars-precedence/)


### Secretos

Mecanismo ofrecido por docker para trabajar con valores sensibles. Contraseñas, certificados, etc.

Los secretos solo son utilizables en forma de archivo. Para utilizarlos es necesario declararlos como un recurso y luego asociarlo al contenedor en cuestión

db_password.txt
```txt
5Uo48J&eE8Ex8zt5jdfQ!MHS
```


```yaml
version: '3.8'

services:
    db:
        image: postgres:15.4
        secrets:
        - db_password

secrets:
   db_password:
     file: db_password.txt
```

Algo importante a tener en cuenta es que, a diferencia de las variables de ambiente, los secretos son montados como un archivo dentro del filesystem del contenedor. En el caso de Docker, los secretos van a estar siempre montado en `/run/secrets/<secret_name>`.  Por lo tanto es importante que la aplicación sepa de la existencia y ubicación de este archivo. En el caso de Postgres este nos permite informarle mediante variable de ambiente donde esta el archivo que contiene el valor en cuestión.


```yaml
version: '3.8'

services:
    db:
        image: postgres:15.4
        environment:
            POSTGRES_PASSWORD_FILE: /run/secrets/db_password
        secrets:
        - db_password

secrets:
   db_password:
     file: db_password.txt
```

> **Desafío**
>
> Como podría hacer para desde la terminal conectarme a la base de datos que levantamos?
>
> Limitaciones:
>
> - Usando psql
> - No hay que forwardear el puerto del contenedor


> **Secretos?**
>
> Si bien compose ofrece la funcionalidad de secretos, la implementación [no brinda las mismas garantias al ser utilizadas via Compose](https://github.com/moby/moby/issues/40046#issuecomment-538777305) que via [Swarm](https://docs.docker.com/engine/swarm/). De todas formas, desacoplar los secretos es **crucial** para tener sistemas seguros y resistentes. Es mucho más riesgoso tener los secretos como parte del código que gestionados de forma aislado con herramientas como [Vault](https://www.vaultproject.io/), [AWS Secrets Manager](https://aws.amazon.com/es/secrets-manager/), entre otros.

## Ejercicio

Replicar el ejercicio realizado la clase anterior utilizando Docker compose. 

- Levantar Postgresql y el Pgadmin. 
- Mantener la red interna
- Incorporar el concepto de volúmenes de Docker para la persistencia de la DB.
- Incorporar los secretos via archivos