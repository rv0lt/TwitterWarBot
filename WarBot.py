#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Proyecto del bot de Twitter de WarBot

import tweepy
import time
from datetime import datetime
import random
import codecs
LIMIT_TWEETS=140 #Limite caracteres en un tweet
SLEEP_TIME=30 #Tiempo que duerme entre mensajes

print('This is my twitter warbot')
# Estas claves se le piden a Twitter para poder funcionar el bot

CONSUMER_KEY = '--'
CONSUMER_SECRET = '--'
ACCESS_KEY = '-----'
ACCESS_SECRET = '--'


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
    self.aliado=""

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
    Aaron; le ha rajado en el poligono;3
    '''
    f = open("jugadores.txt", "r")
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
    id_tweet= api.update_status(text).id_str
    time.sleep(SLEEP_TIME)
    text=""
    contador=0
    while contador < len(jugadores)-1:
        nombre=names[contador]
        if len(text) + len(nombre) > LIMIT_TWEETS:
            print(text + "\n")
            time.sleep(SLEEP_TIME)
            id_tweet = api.update_status(text, id_tweet).id_str #reply al tweet anterior
            text=""
        text+= nombre + ", "
        contador+=1
    nombre=names[contador]
    if len(text) + len(nombre) > LIMIT_TWEETS:
        print(text + "\n")
        time.sleep(SLEEP_TIME)
        id_tweet = api.update_status(text, id_tweet).id_str #reply al tweet anterior
        print(nombre)
        time.sleep(SLEEP_TIME)
        api.update_status(nombre, id_tweet)        
    else:
        text+=nombre
        print(text + "\n")
        time.sleep(SLEEP_TIME)
        id_tweet = api.update_status(text, id_tweet) #reply al tweet anterior

 
    # Iniciamos el bucle que va a ejecutar el programa publicando los ataques
    while len(jugadores) > 1:
        suicidio=False
        recuperar=False
        alianza=False
        # Igualamos 'a' a 'b' para asegurarnos que despues no lo sean
        a = b = 0
        print (a, b)
        # Calculamos los nuevos valores de 'a' y 'b'
        while (a == b) or (jugadores.get(names[a]).aliado==jugadores.get(names[b]).name):
            a = random.randint(0, len(jugadores) - 1)
            b = random.randint(0, len(jugadores) - 1)
            c = random.randint(0, 20)
        #5% posibilidades de recuperar vida y no atacar
        if c==20:
            recuperar=True
        #5% de posibilidades de suicidarte
        elif c==8:
            a=b
            suicidio=True
        #5% de posibilidades de crear alianza en vez de atacar
        elif c==10:
            alianza=True

        foto="media/" + str(c) + ".jpg"
        atacado=jugadores.get(names[b])
        atacante=jugadores.get(names[a])
        print(atacante.name)
        print(atacado.name)
        print (a, b)
        # Restamos una vida al jugador que va a ser atacado y guardamos en el fichero el nuevo valor
        #Si van a ser aliados no modifico nada
        if not alianza:
            vidas_old=atacado.lifes
            if recuperar:
                atacado.lifes+=1
            else:
                atacado.lifes-=1
            vidas_new=atacado.lifes
            f = open("jugadores.txt", "r+")
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
            lineas[b+offset] = lineas[b+offset].replace(str(vidas_old),str(vidas_new))
            print("Aliado del atacante: " + atacante.aliado)
            print("Aliado del atacado: " + atacado.aliado)
            f.writelines(lineas)
            f.close
        #Si van a ser aliados rompen sus alianzas anteriores y se alian
        else:
            if atacado.aliado != "":
                aliado_previo = atacado.aliado
                jugadores.get(aliado_previo).aliado=""
            if atacante.aliado != "":
                aliado_previo = atacante.aliado
                jugadores.get(aliado_previo).aliado=""
            atacado.aliado=atacante.name
            atacante.aliado=atacado.name
        #Si recupera vida
        if recuperar:
            text= "¡MILAGRO! "+ atacado.name + " HA CONSEGUIDO UNA VIDA\nAhora tiene:" + str(atacado.lifes)
            print(text)
            time.sleep(SLEEP_TIME)
            print ("1 seg para publicar\n")
            api.update_with_media(foto,text)  
        #Si se forja una alianza
        elif alianza:
            text= atacante.name + " y " + atacado.name + " ahora son aliados (rompiendo previas alianzas que tuvieran)\nNo se van a atacar entre ellos hasta que sean los ultimos jugadores vivos"    
            print(text)
            time.sleep(SLEEP_TIME)
            api.update_with_media(foto,text)     
        # Si no tiene más vidas twiteamos mensaje de muerte
        elif vidas_new == 0:
            muerte += 1; ataque += 1
            atacante.kills+=1
            if suicidio:
                text=atacante.name + " se ha suicidado\n Quedan " + str(len(jugadores) - 1) + " supervivientes! #WarBot"
            else:
                text= "Siendo la muerte numero: " + str(muerte) + " y el ataque numero: " + str(ataque)+ "\n" + atacante.name + atacante.frase +" a " + atacado.name + " matandole en el acto" + "\n" + atacante.name + " lleva " + str(atacante.kills) + " kill(s).\nQuedan " + str(len(jugadores) - 1) + " supervivientes! #WarBot"
            print (text)
            time.sleep(SLEEP_TIME)
            print ("1 seg para publicar\n")
            api.update_with_media(foto,text)
           
            #Si estaba aliado con alguien se rompe la alianza
            if atacado.aliado != "":
                jugadores.get(atacado.aliado).aliado=""
            # Lo añadimos al array de muertos
            muertos.append(atacado.name)
            # Lo quitamos de los jugadores vivos
            jugadores.pop(atacado.name)
            names.pop(b)
            # Lo guardamos en el fichero para saber quienes ya murieron
            f = open("muertos.txt", "a")
            f.write(muertos[-1] + "\n")
            f.close()
        # Si tiene + vidas twiteamos mensaje de ataque
        else:
            ataque += 1
            if suicidio:
                text=atacante.name + " se ha autolesionado y ha perdido una vida, le quedan: " + str(atacado.lifes) + " vidas.\nQuedan " + str(len(jugadores)) + " supervivientes! #WarBot"
            else:
                text="Siendo el ataque numero: " + str(ataque) + "\n" + atacante.name + atacante.frase + " a " + atacado.name + "\n" + atacado.name + " tiene: " + str(atacado.lifes) + " vidas.\nQuedan " + str(len(jugadores)) + " supervivientes! #WarBot"
            print (text)
            time.sleep(SLEEP_TIME)
            print ("1 seg para publicar\n")
            api.update_with_media(foto,text)
       
        # En caso de quedar 5 jugadores y ser la primera vez en la partida que ocurre se dice quienes quedan
        if len(jugadores) == 5 and flag == 0:
            text="Quedan cinco supervivientes, atentos!!\nSuerte a: " + names[0] + ", " + names[1] + ", " + names[2] + ", " + names[3] + ", " + names[4]
            api.update_status(text)
            print (text)
            flag += 1
        # Si ya se redujo el número de participantes se reinicia flag para cuando queden tres
        elif len(jugadores) == 4:
            flag = 0
        # Si quedan tres participantes y es la primera vez que ocurre se dice quieres quedan
        elif len(jugadores) == 3 and flag == 0:
            text="Quedan tres supervivientes, atentos!!\nSuerte a: " + names[0] + ", " + names[1] + ", " + names[2]
            api.update_status(text)
            print (text)
            flag += 1
        #Se rompen las alianzas que puedan haber
        elif len(jugadores) == 2:
            jugadores.get(names[0]).aliado=""
            jugadores.get(names[1]).aliado=""
        # Se dice quien es el ganador y se le da la Enhorabuena a los dos siguientes clasificados
        elif len(jugadores) == 1:
            text = "Tenemos un ganador!! El ganador es... " + names[0]
            print (text)
            api.update_status(text)
            text="Enhorabuena por el top 3 a: " + muertos[-1] + ", " + muertos[-2] + "\nMuchas gracias a todas y a todos por participar!!"
            print (text)
            api.update_status(text)
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
        #Cada 15 turnos recuerdo las vidas siempre que haya más de un jugador
        if contador_turno % 15 == 0 and len(jugadores)>1:

            text="De momento a los participantes les quedan las siguientes vidas:\n"
            print(text)
            id_tweet= api.update_status(text).id_str
            time.sleep(SLEEP_TIME)
            text=""
            contador=0
            while contador < len(jugadores)-1:
                nuevo = names[contador] + ":" + str (jugadores.get(names[contador]).lifes) + ", "
                if len(text) + len(nuevo) > LIMIT_TWEETS:
                    print(text + "\n")
                    time.sleep(SLEEP_TIME)
                    id_tweet = api.update_status(text, id_tweet).id_str #reply al tweet anterior
                    text=""
                text+= nuevo
                contador+=1
            nuevo = names[contador] + ":" + str (jugadores.get(names[contador]).lifes) 
            if len(text) + len(nuevo) > LIMIT_TWEETS:
                print(text + "\n")
                time.sleep(SLEEP_TIME)
                id_tweet = api.update_status(text, id_tweet).id_str #reply al tweet anterior
                print(nuevo)
                time.sleep(SLEEP_TIME)
                api.update_status(nuevo, id_tweet).id_str #reply al tweet anterior
            else:
                text+=nuevo
                print(text)
                time.sleep(SLEEP_TIME)
                api.update_status(text, id_tweet) #reply al tweet anterior                 

        # Si ya pasaron las horas me duermo 
        if datetime.now().hour == 1:
            
            print ("Descansito ")
            time.sleep(60*60*6)

        #Tiempo que pasa entre ataques
        if contador_turno <= 10 or len(jugadores) <= 4:
            time.sleep(60*30)
        else:
            time.sleep(60*60)

        contador_turno += 1
        print (contador_turno)

# Llamamos a la función para que comience el ataque
muertes()
