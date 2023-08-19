import requests, os, csv, re
from bs4 import BeautifulSoup
# -*- coding: utf-8 -*-


# os.system('cls')

def version1x2(url, Elementos1x2, accion=1, filtro = 70):
  global soup
  # accion = 1 Guarda los valores a archivo
  # accion = 2 Solo muestra en pantalla valores
  # accion = 3 Además de mostrar los valores los filtra por probabilidad
  # accion = 4 es la opción 3 sin imprimir
  # accion = 5 Filtra por probabilidad y guarda en archivo

  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')

  equipos1x2  = funcionSoup(Elementos1x2['equipos']['Links'],Elementos1x2['equipos']['tag'])
  ganador1x2  = funcionSoup(Elementos1x2['ganador']['Links'],Elementos1x2['ganador']['tag'])
  probabilidad1x2  = funcionSoup(Elementos1x2['probabilidad']['Links'],Elementos1x2['probabilidad']['tag'])
  fecha1x2  = funcionSoup(Elementos1x2['fecha']['Links'],Elementos1x2['fecha']['tag'])

  partido = []
  cantidad = len(probabilidad1x2)
  i = 0
  encuentros = []
  while i < cantidad:
    prob = int(probabilidad1x2[i][16:-1])
    if accion in (3,4,5) and prob < filtro:
      i += 1
      continue
    partido = {"Equipo1": equipos1x2[i*2],
              "Equipo2": equipos1x2[i*2+1],
              "Ganador": int(ganador1x2[i]),
              "Probabilidad": prob,
              "Fecha": fecha1x2[i],
              }

    encuentros.append(partido)
    partido = {}
    i += 1

  if accion in (1,5):
    if os.path.exists('Pronosticos/CVS Files/futbol.csv'):
      conf = True
    else:
      conf = False

    with open('Pronosticos/CVS Files/futbol.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        
        if conf == False:
          writer.writerow(['Equipo 1', 'Equipo 2', 'Ganador', 'Probabilidad', 'Fecha'])
        
        for partido in encuentros:
            writer.writerow([partido['Equipo1'], partido['Equipo2'], partido['Ganador'], partido['Probabilidad'], partido["Fecha"]])
  
  if accion in (2,3):
    col = 30
    for partido in encuentros:
      print(f'{partido["Equipo1"]:<{col}} | {partido["Equipo2"]:<{col}} | {partido["Ganador"]:<{5}} | {partido["Probabilidad"]:<{5}}| {partido["Fecha"]}')
  
  return encuentros
#
def funcionSoup(Elementos, tag):
  elemLinks = soup.find_all(tag,Elementos)
  elem = []
  for link in elemLinks:
    elem.append(link.text)
  return elem
# 
def versionProbabilidad(urlCuota, ElementoCuota, base, impresion=True):
  response = requests.get(urlCuota)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')
  data = soup.find_all(ElementoCuota['tag'],ElementoCuota['Links'])

  direcciones = []
  for datos in data:
    texto = str(datos)
    texto = texto.replace('<span class="font-medium w-full lg:w-1/2 text-center dark:text-white">','')
    texto = texto.replace('<a class="" href="','')
    texto = texto.replace('</a>','')
    texto = texto.replace('/">','')
    texto = texto.replace('</span>','')
    texto = texto.strip()
    link, equipos = texto.split("\n")
    link = base + link
    diccionario = {'Equipo': equipos, 'Link': link}
    direcciones.append(diccionario)
    diccionario = {}


  if impresion == True:  
    col = 30
    for partido in encuentros:
      print(f'{partido["Equipo1"]:<{col}} | {partido["Equipo2"]:<{col}} | {partido["Ganador"]:<{3}} | {partido["Probabilidad"]:<{5}}| {partido["Fecha"]}')
      
  return encuentros
#
def pronYprobab():
  global encuentros, encuentrosProbabilidad
  # SECCION - pronosticos - sportytrader - futbol
  url = "https://www.sportytrader.com/es/pronosticos/futbol/"
  Elementos1x2 = {'equipos': {'Links': {'class' : "mx-1 flex items-center dark:text-white"}, 'tag': 'span'},
                  'ganador': {'Links': {'class' :"flex justify-center items-center h-7 w-6 rounded-md font-semibold bg-primary-green text-white mx-1"}, 'tag': 'span'},
                  'probabilidad': {'Links': {'class' :"text-xs mt-1 dark:text-white"}, 'tag': 'span'},
                  'fecha': {'Links': {'class' :"text-xs dark:text-white"}, 'tag': 'span'},
  }
  encuentros = version1x2(url, Elementos1x2, 5)

  # SECCION - probabilidades - sportytrader - futbol
  urlProbabilidad = "https://www.sportytrader.com/es/apuestas/futbol/"
  ElementoProbabilidad = {'Links': {"class" : "font-medium w-full lg:w-1/2 text-center dark:text-white"}, 'tag': 'span'}
  base = 'https://www.sportytrader.com'

  encuentrosProbabilidad = versionProbabilidad(urlProbabilidad, ElementoProbabilidad, base, True)
#

pronYprobab()