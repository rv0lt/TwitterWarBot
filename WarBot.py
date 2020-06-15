#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Proyecto del bot de Twitter de WarBot

import tweepy
import time
import random
import codecs
import sys
LIMIT_TWEETS=140 #Limite caracteres en un tweet


print('This is my twitter warbot')
# Estas claves se le piden a Twitter para poder funcionar el bot
CONSUMER_KEY = 'F9VYQEIKfUZqs0i8DrBZRC9N6'
CONSUMER_SECRET = 'TlMVkv0GEPQ3LgsbtINSbxYDCd7iQnUIO4zliBNwiQ93SNQnD8'
ACCESS_KEY = '1271875353351421952-X8s83Hf5uiU8Bk3UkEDEN4zjwsLyxb'
ACCESS_SECRET = 'O3Xk3QTCPffZQ8XHLeZOxJf7dWED0wIDuNVquUMXjMaCb'


# Linkeamos las claves a la api, para poder Twitear
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
# Clase que va a contener a cada jugador
class Jugador:
  def __init__(self, name, frase, lifes):
    self.name = name
    self.frase= frase
    self.lifes = lifes
    self.kills = 0

# Función principal para ayudar a la moduladidad
def muertes():
    #Jugadores = ["Troma", "Aaron", "Dani", "Guisell", "Iyo", "Max", "Raul", "Yanran", "Andrea", "Alex", "Limon", "Gema", "JC", "Alvaro", "Xiao jing"]
    #Array con los nombres de los jugadores
    names=[]
    #Diccionaria que relaciona el nombre de cada jugador con un objeto Jugador
    jugadores={}
    '''
    El archivo jugadores debe contener en cada línea: Nombre; frase con la que ataque; vidas iniciales
    Ejemplo:
    Aaron; le ha rajado en el poligino;3
    '''
    f = codecs.open("jugadores.txt", "r", "utf-8")
    linea = f.readlines()
    for jugador in linea:
        aux = jugador.split(";")
        names.append(aux[0])
        jugadores[aux[0]] = Jugador(aux[0],aux[1],int (aux[2]))
    f.close
    print (len(jugadores))
    #print(jugadores)
    print(names)
    # Array con los muertos
    muertos = []
    '''
    Abrimos el archivo que contiene las variables con el contador, el flag, ataque y muerte para iniciar o recuperar la
    partida
    '''
    f = open("contador.txt", "r")
    dato = f.readlines()
    contadores = []
    for linea in dato:
        contadores.append(linea[:-1])
    contador_turno = int(contadores[0])
    flag = int(contadores[1])
    ataque = int(contadores[2])
    muerte = int(contadores[3])
    print (contador_turno, flag, ataque, muerte)
    f.close()
    
    #Mensaje de bienvenida
    text= "¡Vamos a comenzar!, nuestros participantes son:\n"
    print(text)
#    id_tweet= api.update_status(text).id_str
    time.sleep(10)
    text=""
    contador=0
    while contador < len(jugadores)-1:
        nombre=names[contador]
        if len(text) + len(nombre) > LIMIT_TWEETS:
            print(text + "\n")
#            id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior
            text=""
        text+= nombre + ", "
        contador+=1
    nombre=names[contador]
    if len(text) + len(nombre) > LIMIT_TWEETS:
        print(text + "\n")
#        id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior
        print(nombre)
#        api.update_status(nombre, id_tweet)        
    else:
        text+=nombre
        print(text + "\n")
#        id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior

 
    # Iniciamos el bucle que va a ejecutar el programa publicando los ataques
    while len(jugadores) > 1:
        suicidio=False
        # Igualamos 'a' a 'b' para asegurarnos que despues no lo sean
        a = b = 0
        print (a, b)
        # Calculamos los nuevos valores de 'a' y 'b'
        while a == b:
            a = random.randint(0, len(jugadores) - 1)
            b = random.randint(0, len(jugadores) - 1)
            c = random.randint(0, 20)
        #5% de posibilidades de suicidarte
        if c==8:
            a=b
            suicidio=True
        # Restamos una vida al jugador que va a ser atacado y guardamos en el fichero el nuevo valor
        atacado = names[b]
        atacado=jugadores.get(atacado)
        atacante= names[a]
        atacante=jugadores.get(atacante)
        print(atacante.name)
        print(atacado.name)
        print (a, b)
        atacado.lifes-=1
        vidas=atacado.lifes
        f = codecs.open("jugadores.txt", "r+", "utf-8")
        lineas=f.readlines()
        f.seek(0,0)
        encontrado=False
        offset=0
        while not encontrado:
            nombre=lineas[b+offset].split(";")[0]
            if(nombre==atacado.name):
                encontrado=True
            else:
                offset+=1
        print(lineas[b+offset])
        lineas[b+offset] = lineas[b+offset].replace(str(vidas+1),str(vidas))
        print(lineas)
        f.writelines(lineas)
        f.close

        # Si no tiene más vidas twiteamos mensaje de muerte
        if vidas == 0:
            muerte += 1; ataque += 1
            atacante.kills+=1
            if suicidio:
                text=atacante.name + " se ha suicidado\n Quedan " + str(len(jugadores) - 1) + " supervivientes! #WarBot"
            else:
                text= "Siendo la muerte numero: " + str(muerte) + " y el ataque numero: " + str(ataque)+ "\n" + atacante.name + atacante.frase +" a " + atacado.name + " matandole en el acto" + "\n" + atacante.name + " lleva " + str(atacante.kills) + " kill(s).\nQuedan " + str(len(jugadores) - 1) + " supervivientes! #WarBot"
            print (text)
            time.sleep(0)
            print ("1 seg para publicar\n")
            #api.update_status("text")
           
            # Lo añadimos al array de muertos
            muertos.append(atacado.name)
            # Lo quitamos de los jugadores vivos
            jugadores.pop(atacado.name)
            names.pop(b)
            # Lo guardamos en el fichero para saber quienes ya murieron
            f = open("muertos_test.txt", "a")
            f.write(muertos[-1] + "\n")
            f.close()
        # Si tiene + vidas twiteamos mensaje de ataque
        else:
            ataque += 1
            if suicidio:
                text=atacante.name + " se ha autolesionado y le quedan: " + str(atacado.lifes) + " vidas.\nQuedan " + str(len(jugadores)) + " supervivientes! #WarBot"
            else:
                text="Siendo el ataque numero: " + str(ataque) + "\n" + atacante.name + atacante.frase + " a " + atacado.name + "\n" + atacado.name + " tiene: " + str(atacado.lifes) + " vidas.\nQuedan " + str(len(jugadores)) + " supervivientes! #WarBot"
            print (text)
            time.sleep(0)
            print ("1 seg para publicar\n")
#            api.update_status(text)
       
        # En caso de quedar 5 jugadores y ser la primera vez en la partida que ocurre se dice quienes quedan
        if len(jugadores) == 5 and flag == 0:
            text="Quedan cinco supervivientes, atentos!!\nSuerte a: " + names[0] + ", " + names[1] + ", " + names[2] + ", " + names[3] + ", " + names[4]
#            api.update_status(text)
            print (text)
            flag += 1
        # Si ya se redujo el número de participantes se reinicia 'j' para cuando queden tres
        elif len(jugadores) == 4:
            flag = 0
        # Si quedan tres participantes y es la primera vez que ocurre se dice quieres quedan
        elif len(jugadores) == 3 and flag == 0:
            text="Quedan tres supervivientes, atentos!!\nSuerte a: " + names[0] + ", " + names[1] + ", " + names[2]
#            api.update_status(text)
            print (text)
            flag += 1
        # Se dice quien es el ganador y se le da la En Hora Buena a los dos siguientes clasificados
        elif len(jugadores) == 1:
            text = "Tenemos un ganador!! El ganador es... " + names[0]
            print (text)
#            api.update_status(text)
            text="Enhorabuena por el top 3 a: " + muertos[-1] + ", " + muertos[-2] + "\nMuchas gracias a todas y a todos por participar!!"
            print (text)
#            api.update_status(text)
        '''
        Se guardan las variables en el fichero 'contador.txt' para
        restablecer la partida en el punto actual
        '''
        f = open("contador.txt", "w")
        contador_turno += 1
        f.write(str(contador_turno) + "\n")
        contador_turno -= 1
        f.write(str(flag) + "\n")
        f.write(str(ataque) + "\n")
        f.write(str(muerte) + "\n")
        f.close()
        #Cada 10 turnos recuerdo las vidas siempre que haya más de un jugador
        if contador_turno % 10 == 0 and len(jugadores)>1:

            text="vidas:\n"
            print(text)
#            id_tweet= api.update_status(text).id_str
            time.sleep(10)
            text=""
            contador=0
            while contador < len(jugadores)-1:
                nuevo = names[contador] + ":" + str (jugadores.get(names[contador]).lifes) + ", "
                if len(text) + len(nuevo) > LIMIT_TWEETS:
                    print(text + "\n")
#                    id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior
                    text=""
                text+= nuevo
                contador+=1
            nuevo = names[contador] + ":" + str (jugadores.get(names[contador]).lifes) 
            if len(text) + len(nuevo) > LIMIT_TWEETS:
                print(text + "\n")
#                id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior
                print(nuevo)
#                id_tweet = api.update_status(nuevo, id_tweet) #reply al tweet anterior
            else:
                text+=nuevo
                print(text)
#                id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior                 

        # Si ya pasaron las 16 horas (de 9:00 AM a 24:00 PM) me duermo toda la noche
        if contador_turno % 16 == 0:
            print ("Descansito ")
            #time.sleep(60*60*8)

        #Tiempo que pasa entre ataques
        time.sleep(0.5*1)

        contador_turno += 1
        print (contador_turno)

# Llamamos a la función para que comience el ataque
muertes()
