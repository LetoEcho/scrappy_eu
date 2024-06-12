import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# Nombre del archivo de texto
orden='03'
comunidad='andalucia'
provincia='cordoba'
nombre_archivo = orden+comunidad+'-'+provincia+'.txt'

# Lista para almacenar las líneas del archivo
lineas = []

# Abrir el archivo en modo lectura
with open(nombre_archivo, 'r') as archivo:
    # Iterar sobre cada línea del archivo
    for linea in archivo:
        # Eliminar los espacios en blanco al principio y al final de la línea y agregarla a la lista
        lineas.append(linea.strip())

# Ahora tienes todas las líneas del archivo almacenadas en la lista 'lineas'
# Puedes acceder a cada línea individualmente usando índices de lista
# Por ejemplo, para acceder a la primera línea:
primera_linea = lineas[0]

for linea in lineas:
# Navegar a la página web
    base_url = 'https://elpais.com' + linea

    # Configurar el servicio de ChromeDriver
    service = Service(ChromeDriverManager().install())

    # Inicializar el navegador
    driver = webdriver.Chrome(service=service)
    # Formatear las partes del URL con ceros iniciales

    try:
        # Navegar a la página web
        driver.get(base_url)

        # Esperar hasta que la tabla específica esté presente
        wait = WebDriverWait(driver, 2)
        accept_cookies_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='pmConsentWall-button' and text()='Aceptar y continuar']")))

        # Hacer clic en el botón de aceptación de cookies
        accept_cookies_button.click()

        municipio_element = driver.find_element(By.CLASS_NAME, 'd_t')

        # Obtener el texto del nombre del municipio
        municipio_nombre = municipio_element.text.split('/')[0].strip()  # Eliminar "/ Municipio" y espacios en blanco

        print("Nombre del municipio:", municipio_nombre)

        tabla = 'Resultados por partido en ' + municipio_nombre
        print(tabla)
        # Utiliza format() para insertar el valor de tabla en el XPath
        xpath_selector = "//table[caption[text()='{}']]".format(tabla)

        # Esperar hasta que la tabla específica esté presente
        table = wait.until(EC.presence_of_element_located((By.XPATH, xpath_selector)))

        lista_partidos=['FO','AGRUPACIÓN DE ELECTORES SE ACABÓ LA FIESTA','IZQESP','PP','PSOE','VOX','SUMAR','PODEMOS']
        for partido in lista_partidos:
            try:
                xpath_partido=".//tr[th[abbr='{}']]".format(partido)

                # Encontrar la fila correspondiente al partido actual
                partido_row = table.find_element(By.XPATH, xpath_partido)

                # Extraer los valores de votos y porcentaje
                votos_2024 = partido_row.find_element(By.XPATH, "./td[1]/span").text
                porcentaje_2024 = partido_row.find_element(By.XPATH, "./td[2]/span").text
                porcentaje_sin_simbolo = porcentaje_2024.rstrip('%').strip()

                print("Votos "+partido+" 2024:", votos_2024)
                print("Porcentaje "+partido+" 2024:", porcentaje_sin_simbolo)

                # Nombre del archivo CSV
                nombre_archivo_csv = 'datos_municipios.csv'

                # Escribir los datos en un archivo CSV
                with open(nombre_archivo_csv, 'a', newline='', encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv, delimiter='|')
                    # Escribir los datos
                    escritor_csv.writerow([comunidad,provincia,municipio_nombre, partido,votos_2024, porcentaje_sin_simbolo])

                print("Los datos han sido guardados en el archivo:", nombre_archivo_csv)

            except Exception:
                print(f"No se encontró el partido {partido} en la página: {base_url}")
                # Nombre del archivo CSV
                nombre_archivo_csv = 'datos_municipios.csv'

                # Escribir los datos en un archivo CSV
                with open(nombre_archivo_csv, 'a', newline='', encoding='utf-8') as archivo_csv:
                    escritor_csv = csv.writer(archivo_csv, delimiter='|')
                    # Escribir los datos
                    escritor_csv.writerow([comunidad,provincia,municipio_nombre,partido, 0, 0])
                # Continuar con el siguiente partido

    except TimeoutException:
            print(f"No se pudieron encontrar los elementos en el tiempo especificado para la URL: {base_url}")
            # Nombre del archivo CSV
            nombre_archivo_csv = 'datos_municipios.csv'

            # Escribir los datos en un archivo CSV
            with open(nombre_archivo_csv, 'a', newline='', encoding='utf-8') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv, delimiter='|')
                # Escribir los datos
                escritor_csv.writerow([comunidad,provincia,municipio_nombre, partido,votos_2024, porcentaje_sin_simbolo])
            
    except Exception as e:
            print(f"Error en la URL: {base_url} - {str(e)}")  
            # Nombre del archivo CSV
            nombre_archivo_csv = 'datos_municipios.csv'

            # Escribir los datos en un archivo CSV
            with open(nombre_archivo_csv, 'a', newline='', encoding='utf-8') as archivo_csv:
                escritor_csv = csv.writer(archivo_csv, delimiter='|')
                # Escribir los datos
                escritor_csv.writerow([comunidad,provincia,municipio_nombre,partido, 0, 0])

    driver.quit()


