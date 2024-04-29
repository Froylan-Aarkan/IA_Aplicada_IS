#arreglo de 10 posiciones con valores aleatorios en cada posicion.
#cruza: BLX-a
#Seleccion de padres mediante una ruleta
#Mutacion uniforme
#Incluir uso de elitismo: elegir al mejor de los padres y mantenerlo.

#Realizar 30 ejecuciones 
#entrega: 23 de abril

import random
import math

#Parametros del algoritmo genetico
TAMANIO_POBLACION = 10
GENERACIONES = 10000
RATIO_MUTACION = 1
RATIO_CRUZA = 0.5
ALPHA = 0.5

#Limites y precisión
RANGO_MINIMO = -5.12
RANGO_MAXIMO = 5.12
PRECISION = 3
TAMANIO_INDIVIDUO = 10

def generar_individuo():
    return [round(random.uniform(RANGO_MINIMO, RANGO_MAXIMO), PRECISION) for _ in range(TAMANIO_INDIVIDUO)]

def generar_poblacion():
    return [generar_individuo() for _ in range(TAMANIO_POBLACION)]

def funcion_aptitud(individuo):
    aptitud = 0
    for i in individuo:
        aptitud  = aptitud + (i ** 2) - (10 * math.cos(2 * math.pi * i))

    aptitud = (10 * TAMANIO_INDIVIDUO) + aptitud

    return aptitud

def cruza_BLX(padre1, padre2):
    hijo = []
    for i in range(TAMANIO_INDIVIDUO):
        c_minimo = min(padre1[i], padre2[i])
        c_maximo = max(padre1[i], padre2[i])
        intervalo = c_maximo - c_minimo
        valor_minimo = c_minimo - ALPHA * intervalo
        valor_maximo = c_maximo + ALPHA * intervalo
        hijo.append(round(random.uniform(valor_minimo, valor_maximo), PRECISION))

    return hijo

def mutacion_uniforme(individuo):
    individuo_mutado = individuo.copy()
    for i in range(TAMANIO_INDIVIDUO):
        if random.random() < RATIO_MUTACION:
            individuo_mutado[i] = round(random.uniform(RANGO_MINIMO, RANGO_MAXIMO), PRECISION)

    return individuo_mutado

#Implementacion de DeJong
def seleccion_padres_ruleta(suma_aptitud, poblacion):
    suma = 0
    r = round(random.uniform(0, suma_aptitud), PRECISION)
    for i in poblacion:
        aptitud_individuo = funcion_aptitud(i)
        suma = suma + aptitud_individuo
        if suma >= r:
            return i


def suma_aptitud_poblacion(poblacion):
    suma_aptitud = 0
    for i in poblacion:
        aptitud_individuo = funcion_aptitud(i)
        suma_aptitud = suma_aptitud + aptitud_individuo

    return suma_aptitud

def algoritmo_genetico():
    poblacion = generar_poblacion()
    print("Individuo inicial: ", poblacion[0])
    print("Aptitud del individuo inicial: ", funcion_aptitud(poblacion[0]))

    for generacion in range(GENERACIONES):
        poblacion_nueva = []

        #Uso de elitismo para el mejor individuo de la anterior poblacion
        poblacion_nueva.append(min(poblacion, key=funcion_aptitud))

        for _ in range(TAMANIO_POBLACION - 1):
            padre1 = seleccion_padres_ruleta(suma_aptitud_poblacion(poblacion), poblacion)
            padre2 = seleccion_padres_ruleta(suma_aptitud_poblacion(poblacion), poblacion)
            hijo1 = cruza_BLX(padre1, padre2)
            hijo2 = cruza_BLX(padre1, padre2)
            hijo1 = mutacion_uniforme(hijo1)
            hijo2 = mutacion_uniforme(hijo2)
            poblacion_nueva.extend([hijo1, hijo2])

        poblacion = poblacion_nueva
        mejor_individuo = min(poblacion, key=funcion_aptitud)
        print("Generación:", generacion+1, "- Mejor individuo:", mejor_individuo, "- Valor de aptitud:", round(funcion_aptitud(mejor_individuo), PRECISION))

    mejor_individuo = min(poblacion, key=funcion_aptitud)
    return mejor_individuo, round(funcion_aptitud(mejor_individuo), PRECISION)

mejor_solucion, mejor_aptitud = algoritmo_genetico()
print("Mejor solucion: ", mejor_solucion)
print("Valor de aptitud: ", mejor_aptitud)