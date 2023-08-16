import requests, os, csv
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-


# os.system('cls')

url = "https://www.sportytrader.com/es/pronosticos/tenis/"

response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

Elementos = {'liga': {'Links':{ "class":"text-balance tex-center block px-10"}, 'tag': "span"},
             'equipos': {'Links': {"class":"font-semibold text-center flex min-h-[45px] dark:text-white"}, 'tag': "span"},
             'pronosticos': {'Links': {"class":"text-center font-semibold"}, 'tag': "p"},
             'fecha': {'Links': {"text-center text-xs mt-2 dark:text-white"}, 'tag': "p"},
}




def funcionSoup(Elementos, tag):
  elemLinks = soup.find_all(tag,Elementos)
  elem = []
  for link in elemLinks:
    elem.append(link.text)
  return elem
#
def versionPronosticos(accion=1):
  # accion = 1 Guarda los valores a archivo
  # accion = 2 Solo muestra en pantalla valores

  liga = funcionSoup(Elementos['liga']['Links'],Elementos['liga']['tag'])
  equipos  = funcionSoup(Elementos['equipos']['Links'],Elementos['equipos']['tag'])
  pronosticos  = funcionSoup(Elementos['pronosticos']['Links'],Elementos['pronosticos']['tag'])
  fecha =funcionSoup(Elementos['fecha']['Links'],Elementos['fecha']['tag'])

  partido = []
  cantidad = len(liga)
  i = 0
  encuentros = []
  while i < cantidad:
    
    busqueda = f"{liga[i]} {equipos[i*2]} vs {equipos[i*2+1]} resultado"
    url = f"https://www.google.com/search?q={busqueda}"

    busqueda_codificada = requests.utils.quote(busqueda)
    enlace_busqueda = f"https://www.google.com/search?q={busqueda_codificada}"

    partido = {"liga": liga[i],
              "Equipo1": equipos[i*2],
              "Equipo2": equipos[i*2+1],
              "Pronósticos": pronosticos[i],
              "Fecha": fecha[i],
              "Enlace_Busqueda": enlace_busqueda,
              }

    encuentros.append(partido)
    partido = {}
    i += 1

  if accion != 1:
    col =30
    for partido in encuentros:
      print(f'{partido["liga"]:<{col}} | {partido["Equipo1"]:<{col}} | {partido["Equipo2"]:<{col}} | {partido["Fecha"]:<{col}}| {partido["Pronósticos"]:<{col}}')
      print(f'{partido["Enlace_Busqueda"]}')
  
  else:
    if os.path.exists('Pronosticos/pronosticos.csv'):
      conf = True
    else:
      conf = False

    with open('Pronosticos/pronosticos.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        
        if conf == False:
          writer.writerow(['Liga', 'Equipo 1', 'Equipo 2', 'Pronósticos', 'Fecha', 'Enlace de Busqueda'])
        
        for partido in encuentros:
            writer.writerow([partido['liga'], partido['Equipo1'], partido['Equipo2'], partido['Pronósticos'], partido['Fecha'], partido["Enlace_Busqueda"]])
#

versionPronosticos(1)