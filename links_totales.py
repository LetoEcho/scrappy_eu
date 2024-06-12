from bs4 import BeautifulSoup
import requests

# URL de la página web
url = 'https://elpais.com/internacional/elecciones/europeas/19/08/49/'

# Realizar la solicitud GET a la página web
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Crear un objeto BeautifulSoup para analizar el HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todas las etiquetas option
    options = soup.find_all('option')

    # Nombre del archivo de texto
    nombre_archivo = 'hrefs_municipios.txt'

    # Abrir el archivo en modo de anexión
    with open(nombre_archivo, 'w') as archivo:
        # Iterar sobre todas las etiquetas option
        for option in options:
            # Obtener el valor del atributo href
            href = option.get('value')

            # Verificar si href no es None antes de concatenarlo
            if href is not None:
                # Escribir el valor del atributo href en el archivo
                archivo.write(href + '\n')

    print("Los hrefs han sido guardados en el archivo:", nombre_archivo)
else:
    print("Error al obtener la página:", response.status_code)
