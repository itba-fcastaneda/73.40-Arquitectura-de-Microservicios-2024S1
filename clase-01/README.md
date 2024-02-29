# Práctica 1 - Introducción a Docker

## Instalando Linux - Ubuntu 22.04.2

En primer lugar debemos obtener la imagen de Ubuntu, que puede ser descargada de los siguientes links:

**x86**

[https://ubuntu.com/download/server](https://ubuntu.com/download/server)

**Apple Silicon**

[https://ubuntu.com/download/server/arm](https://ubuntu.com/download/server/arm)

Existen varias alternativas de máquinas virtuales que se pueden utilizar para instalar la imagen y ejecutar Linux en diferentes arquitecturas, incluyendo ARM y x86. A continuación listamos algunas de ellas:

- **VirtualBox**: Es un software de virtualización desarrollado por Oracle que permite ejecutar sistemas operativos en máquinas virtuales. Es compatible con diferentes arquitecturas, incluyendo ARM y x86. [https://www.virtualbox.org/](https://www.virtualbox.org/)
- **UTM**: Es una herramienta de virtualización de código abierto que se enfoca en la emulación de sistemas operativos para arquitecturas diferentes, incluyendo ARM y x86. UTM se puede utilizar en sistemas operativos como macOS, Linux y Windows: [https://mac.getutm.app/](https://mac.getutm.app/)
- QEMU: Es un software de virtualización de código abierto que permite ejecutar sistemas operativos en diferentes arquitecturas, incluyendo ARM y x86. [https://www.qemu.org/](https://www.qemu.org/)
- VMware Workstation: Es un software de virtualización, pago, que permite ejecutar sistemas operativos en máquinas virtuales. Es compatible con diferentes arquitecturas, incluyendo ARM y x86. [https://www.vmware.com/products/workstation-pro.html](https://www.vmware.com/products/workstation-pro.html)
- KVM: Es un hipervisor de virtualización de código abierto que permite ejecutar sistemas operativos en diferentes arquitecturas, incluyendo ARM y x86. KVM está disponible en diferentes distribuciones de Linux, como Ubuntu, Fedora y CentOS. [https://help.ubuntu.com/community/KVM/Installation](https://help.ubuntu.com/community/KVM/Installation)

> 💡 Al momento de realizar la instalación de Linux, instalaremos dos paquetes importantes para el uso habitual que le daremos a este servidor. En primer lugar instalaremos OpenSSH y luego Docker. Para este último debemos ingresar e instalar la versión estable.
> 
> 
> ![Menu](imgs/menu.png)
> 
> ![OpenSSH](imgs/openssh.png)
> 

Una vez completada la instalación de Linux, accedemos al prompt con nuestro usuario y contraseña, definidos en el proceso de instalación, y procedemos a actualizar todos los paquetes del sistema mediante el siguiente comando:

```bash
sudo apt-get update
```

Además de actualizar los paquetes de Linux, ejecutar este comando también nos permitirá verificar que nuestra máquina virtual está conectada a la red.

Para comprobar si Docker está instalado en nuestra máquina virtual, podemos utilizar el siguiente comando:

```bash
docker
```

Mostrará  los comandos disponibles. Luego, para verificar la instalación, podemos ejecutar el comando:

```bash
sudo docker run hello-world
```

Ejecutará un contenedor con la imagen "hello-world" y mostrará un mensaje de éxito en la consola.

## Docker en accion

> OBJETIVO
>
> Levantar una base de datos Postgres y una instancia de PGAdmin para consultarla.
> Las bases de datos no deben ser accesibles desde afuera, sólo el manager.

Dado que queremos aislar la DB pero que pgadmin se pueda conectar vamos a crear una red interna

```bash
docker network create --internal db_net
```

Luego, dado que vamos a utilizar una base de datos y queremos que la información sea persistente, vamos a crear un volumen

```bash
docker volume create db_vol
```

Ahora podemos levantar la DB

```bash
docker run -d --rm \
    -e POSTGRES_USER=robin \
    -e POSTGRES_PASSWORD=papanata \
    -v db_vol:/var/lib/postgresql/data \
    --name db \
    --network db_net \
    postgres:16
```

Levantamos un contenedor: en background (`-d`), indicamos que queremos que sea borrado una vez detenido (`--rm`) le pasamos como variable de entorno el nombre y la password del superUser (`-e POSTGRES_USER=robin`, `-e POSTGRES_PASSWORD=papanata`), le asignamos el volumen creado (`-v db_vol:/var/lib/postgresql/data`), lo asociamos a la red generada previamente (`--network db_net`) y le definimos un nombre para poder referenciarlo en posteriores comandos (`--name db`).

Ahora vamos a levantar la instancia de pgadmin

```bash
docker run -d --rm \
    -e PGADMIN_DEFAULT_EMAIL=user@itba.edu \
    -e PGADMIN_DEFAULT_PASSWORD=p4ssw0rd \
    --name pgadm \
    -p 5050:80 \
    dpage/pgadmin4
```

En el caso del contenedor de pgadmin este lo levantaremos en la red default ya que **necesitamos que se encuentre en una red NO interna** para poder exponer su puerto (`-p 5050:80`).

Luego, para que el contenedor de pgadmin pueda comunicarse con la DB necesitamos que compartan red.

```bash
docker network connect db_net pgadm
```

> Podemos verificar que el contenedor se encuentra asociado a 2 redes utilizando
> `docker exec -ti pgadm ip a`
> Ademas de la red loopback se deberían ver 2 interfaces más.
> Realizando la misma prueba con el contenedor de la db deberían ver la interfaz de loopback y solo una mas.

Terminada esta configuración tienen que poder acceder a pgadmin en localhost:5050. Utilizando las credenciales definidas como env al levantar los containers. En caso de correr docker en un servidor remoto pueden hacer un tunel ssh y accederlo de forma local (`-L 5050:localhost:5050`)



## Entendiendo como Docker funciona por dentro

### Usuarios

Si nosotros pensamos a los contenedores como maquinas virtuales podriamos concluir que los usuarios que van a existir dentro de los mismos no tienen ningun tipo de conexion con los usuarios del host. En el caso de los contenedores, el proceso que se va a estar ejecutando lo estara haciendo de forma directa sobre el host. Hagamos algunas pruebas para verificarlo.

```bash
docker run -d ubuntu:latest sleep 500
ps uxa | grep sleep
```

Al hacer ps en el host podemos ver como aparece el proceso de sleep que ejecutamos dentro del container. Algo que llama la atencion es que el proceso esta siendo corrido por el usuario root. Esto se debe a que los containers utilizan el mismo sistema de UIDs que el kernel host. Por defecto al ejecutar un container este tomara el valro 0 asociado al usuario root. Podemos ver como esto cambia utilizando el flag `--user <name|uid>`

```bash
docker run -d --user 1234 ubuntu:latest sleep 500
ps uxa | grep sleep
```

Podemos ver como el proceso actual aparece con el usuario 1234, el mismo que indicamos antes. Asi como en este caso usamos el userID 1234, se podria usar cualquier otro. Esta es una de las consideraciones a tener en cuenta a la hora de correr un container. Si bien son un proceso aislado, tiene cierto contacto con el host subyacente. Un caso donde hay que tener en cuenta los usuarios son los permisos de los archivos y directorios.

### Network

En el contexto de los microservicios y las aplicaciones en general, muchas veces queremos exponer servicios para que sean accedidos por otros servicios o usuarios finales. Para esto la opcion mas utilziada es exponer un puerto y comunicarse via TCP/UDP. Que sucede con los containers?

Asi como los containers estan aislados a nivel filesystem y proceso tambien lo estan a nivel networking. Cada container tendra su propia interfaz de red. A su vez, docker nos permite generar multiples redes virtuales, permitiendo aislar a los contenedores del resto.

Teniendo en cuenta esto, como es posible acceder a los contenedores? Es siquiera posible?

Vamos a crear levantar un contenedor con un nginx adentro y vamos a verificarlo.

```bash
docker run --name web_server -d nginx
sudo ln -sf /proc/$(docker inspect -f '{{.State.Pid}}' web_server)/ns/net /var/run/netns/mycontainer; sudo ss -tln -N mycontainer ; sudo rm /var/run/netns/mycontainer
```

Despues de haberme mandado su contraseña con ese segundo comando, deberian ver que en el purto 80 hay un proceso escuchando. Lo que estamos haciendo ahi es analizando los puertos ocupados en la interfaz de red del container. Nginx esta corriendo y esperando conexiones. Si en vez de correr el segundo comando corremos `ss -nlt` en nuestro host veremos que no hay nadie en el puerto 80. Como podemos hacer para llegar?

Si bien no lo vemos a simple vista, el contenedor forma parte de una red virtual de nuestro host y el proceso esta escuchando en todas las interfaces `0.0.0.0:80`. Teniendo en cuenta que la red esta dentro del host y conociendo la IP del contenedor deberiamos poder llegar al nginx. 

```bash
curl $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Efectivamente pudimos acceder al servidor. Esto se debe a que lso container formen parte del host y no sean una abstracion completamente separada. Entonces, si desde el host puedo llegar, donde esta la aislacion? La aislacion que nos interesa es en relacion a otros contenedores, no al host en si. Para eso veamos un ejemplo.

Con el nginx corriendo deberian poder acceder al mismo de la siguiente forma:

```bash
docker run --rm curlimages/curl --silent $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Si dijimos que se aislaba el contenedor de otros contenedores, por que estamos llegando? Si bien a veces es de interes estar aislado, otras veces es de interes acceder otros servicios. Para ello se pueden generar redes que contengan 1 o mas contenedores. Podemos ver que, si creamos una nueva red y levantamos el contenedor de curl en la misma, este no llegara al nginx.

```bash
docker run --rm --network lonely_curl curlimages/curl -v -m 5 $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' web_server)
```

Podemos ver como ahora el curl no funciona y corta por timeout.

```bash
docker run - wbitt/network-multitool ip a
docker run --network lonely_curl wbitt/network-multitool ip a
```

Con estos dos comandos podemos verificar que los containers que se generan dentro de la red lonely_curl efectivamente tienen una red distinta a los que no. Impidiendo la comunicacion entre los mismos.

Pueden limpiar todos los contenedores que se generaron en el camino con `docker rm -f $(docker ps -aq)` 
