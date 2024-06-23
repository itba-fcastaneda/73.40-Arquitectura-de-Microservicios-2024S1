# CI

## GitlabRunner

[Instalar el runner](https://docs.gitlab.com/runner/install/docker.html)

`docker volume create gitlab-runner-config`

```bash
docker run -d --name gitlab-runner --restart always \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v gitlab-runner-config:/etc/gitlab-runner \
    gitlab/gitlab-runner:latest
```

- [Registrar el runner](https://docs.gitlab.com/runner/register/index.html#docker)
- [Variables predefinidas](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)

`docker run --rm -it -v gitlab-runner-config:/etc/gitlab-runner gitlab/gitlab-runner:latest register`

Pide una URL y un Token que se consiguen en `<REPO> > Settings > CI/CD > Runners`, usar `docker` como executor. y `docker:latest` como imagen

Hay que modificar el archivo `config.toml` del runner. Se puede acceder al mismo desde el host (la configuracion se monto como volumen) o desde el container.  Hay que agregar `privileged=true` y en volumes: `["/cache", "/var/run/docker.sock:/var/run/docker.sock"]`.

## Pipeline

Para crear un pipeline dentro de gitlab vamos a definir un archivo llamado `.gitlab-ci.yml` en la raiz del proyecto. En este caso, vamos a usar un pipeline que ejecute en docker, por eso la imagen del mismo sera `image: docker:latest`.

La estructura basica del archivo consiste en:

```yaml
image: docker:latest

variables:
  IMAGE_BASE: "$CI_REGISTRY/$CI_PROJECT_NAMESPACE/$CI_PROJECT_NAME"
  ... 

stages:
  - prep
  - build
  - test
  - deliver
  - deploy

job1:
  ...
job2:
  ...
```
[GitLab CI reference](https://docs.gitlab.com/ee/ci/yaml/)

En este caso estamos declarando la imagen mencionada, declaramos variables a ser utilizadas en el pipeline, definimos el orden y nombre de los stages y declaramos los jobs en cuestión.

En nuestro caso utilizamos un stage llamado `prep` para realizar tareas de preparacion previas a la ejecucion del pipeline. En particular, se utiliza este stage para definir los nombres de todas las imagenes a ser creadas a lo largo del pipeline. Estos valores sera almacendas en un artifact llamado `context.env`. Luego, a medida que sea necesario, cada job solicitara el artifact y obtendra los valores requeridos.

El uso de tags es importante para separar la ejecucion en los distinto ambientes. En este caso, eel ambiente de build + test y el ambiente productivo final.

## Imagenes Docker

La idea de las imagenes es generar imagenes de testing que sean lo mas parecido a la imagen final. En el caso de python, la imagen de testing es una extension de la imagen productiva, se agregan las dependencias de testing y se hacen los ajustes pertinentes.


