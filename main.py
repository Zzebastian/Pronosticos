import csv, os
os.system('cls')
# -*- coding: utf-8 -*-
# import pronosticosYcuotas
# import pronosticosTenis

def Ganador():
    
    with open('Pronosticos/pronosticos1x2.csv', 'r', encoding='utf-8') as f:
        a = csv.reader(f, delimiter=',')
        datos = list(a)

    text = 'De la siguiente lista, devuelve quién ha ganado el encuentro.'
    text += ' La lista contiene además, bajo la columna "Ganador" una predicción de quié ganaría ese encuentro'
    text += 'Además lo quiero en un formato compatible con google sheets, agrega también la fecha de juego '
    text += 'Si el juego no se ha jugado en los últimos 15 días, en vez de un ganador, considera que aún no se ha jugado'
    print(text)
    col =35
    for row in datos:

        try:
            I = int(row[2])
            Win = row[I-1]
        except:
            Win = row[2]

        print(f'{row[0]:<{col}} | {row[1]:<{col}} | {Win}')
#
def Pronosticos():
    
    with open('Pronosticos/pronosticos.csv', 'r', encoding='utf-8') as f:
        a = csv.reader(f, delimiter=',')
        datos = list(a)
        
    text = 'De la siguiente lista, devuelve si el pronóstico ha sido correcto.'
    text += ' Además lo quiero en un formato compatible con google sheets'
    text += ' Agrega una columna para que pueda verificar de que fecha es el encuentro que estàs teniendo en cuenta'
    print(text)
    col =35
    for row in datos:

        try:
            I = int(row[2])
            Win = row[I-1]
        except:
            Win = row[2]

        print(f'{row[0]:<{20}} | {row[1]:<{col}}| {row[2]:<{col}}| {row[3]:<{col}}')#| {row[4]:<{col}}')
#


FF = input('True (1) o False (0) ')
if FF == '1':
    import sportytrader_pronosticos
    import sportytrader_apuestas
Ganador()
print('-----------------------')
Pronosticos()

