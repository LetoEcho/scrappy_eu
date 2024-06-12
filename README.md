
# ScrapPY EU

Con este proyecto se podrán extraer datos de los votos de las elecciones europeas celebradas en el 2024. Se pueden consultar los resultados de los partidos: PP, PSOE, Sumar, Podemos, SALF, Frente Obrero y IzqEsp.




## Cómo empezar

Se necesita tener instalado Python.

Cuando ya esté instalado, se necesitan las siguientes bibliotecas:

```bash
  pip install bs4 requests sellenium webdriver_manager
```


    
## Primeros pasos - links_totales.py - URL de la provincia deseada
Este código cogerá los votos de los municipios de una provincia.

Para sacar los URL de una provincia, depende de los números que se encuentran al final de la URL. Por ejemplo, para la provincia de Huelva, la URL tiene esta pinta: https://elpais.com/internacional/elecciones/europeas/19/01/21/

Cada municipio corresponde con un número después del /21/ en el caso de Huelva. Pero no podemos saber cuántos hay disponibles en la web.

El archivo links_totales.py hace esto.
Tenemos que pegar en la línea 5 la URL de la provincia que interese:
```bash
5    url = URL_PROVINCIA
```

Con esto, ejecutamos el código y guardará todo lo que ha encontrado en los combos en el archivo hrefs_municipios.txt.

De este archivo solo interesa los links que sean iguales a nuestra URL mas el número del municipio y guardar todo esto en un txt aparte con el nombre: XXcomunidad-provincia.txt


## Votos por municipio - scrapp.py
Con este script lanzamos el escaneo de datos que tengan que ver con la provincia que le pasemos y todos sus municipios, guardando en el archivo datos_municipio.csv los resultados de cada partido.

En las líneas siguientes tenemos que poner los datos que tiene nuestro txt con las URL:
```code
11    orden='00'
12    comunidad='nombre-comunidad'
13    provincia='nombre-provincia'
```

Por ejemplo, si mi archivo se llama 01andalucia-almeria.txt, sería:
```code
11    orden='01'
12    comunidad='andalucia'
13    provincia='almeria'
```

Con esto, podemos ejecutar el código e irán apareciendo por consola todos los votos que va encontrando. En el caso de que un partido no aparezca porque no fue votado, el resultado será de 0 votos y 0% de porcentaje.

Todos los datos se pueden ir viendo en el archivo datos_municipio.csv.

## Últimos pasos
Cuando acabe el conteo, para poder asegurarse que se han recorrido todos los municipios del archivo TXT, hay que ver cuántas líneas hay en el archivo por 8 (por partidos) y compararlas con las líneas del archivo datos_municipios.csv (mas 1, sin contar la cabecera).

Por ejemplo, si mi provincia tenia 10 links de municipios, lo multiplico por 8, es decir, 80. Si el archivo datos_municipio tiene 81-1 líneas, el conteo ha sido el correcto.

Ya tenemos los datos.