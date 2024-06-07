# CAMBIOS

## Modificacion del dashboard

Para poder modificar el dashboard de ejemplo hay que ir a la configuracion del dashboard y poner "Save As"

## Query: Healthcheck para las aplicaciones

```pql
(
    sum(rate(health_http_requests_total{result="http_success"}[$__rate_interval])) by (name) 
    - (
        sum(rate(health_http_requests_total{result!="http_success"}[$__rate_interval])) by (name) 
        OR (sum(rate(health_http_requests_total{result="http_success"}[$__rate_interval])) by (name) * 0)
    )
) > bool 0
``` 

la metrica que tenemos es la cantidad de veces que el healthcheck salio bien o mal en funcion del tiempo. La funcion es el valor acumulado. Una forma de detctar que el servicio esta caido es que, la cantidad de healthchecks que fallan estan creciendo y la cantidad que son exitosos no. Una forma de verificar esto es que la derivada (rate) de una metrica sea mayor que la otra.

Dos aclaraciones. El bool 0 del final permite expresar la metrica como un valor booleano, sino el operador de comparacion hace que la metrica se filtrada y no se muestre cuando la condicion no se cumple. Por otro lado, el uso del `OR` es para los casos que un servicio nunca fallo, si bien es raro, eso genera que no haya una segunda metrica para comparar y el resultado no se muestre.