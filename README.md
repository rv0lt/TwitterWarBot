# TwitterWarBot

Proyecto de WarBot para Twitter

El fichero jugadores.txt contiene los jugadores que van a participar en el siguiente formato:

`Nombre; frase con la que ataque; vidas iniciales`

Ejemplo:

`Aaron; le ha rajado en el poligono;3`

Si el servidor se para la partida puede retomarse en el punto donde se paro.

Una vez acabada la partida, los ficheros se reincian con el script reinicio.sh

### Reglas del juego

1. Todo jugador comienza con un numero igual de vidas
2. Cada cierto tiempo se produce un evento que puede ser ataque (85%), Suicidio(5%), Recuperacion(5%) y Alianza (5%)
3. Cada 15 turnos recuerda las vidas de los jugadores vivos
4. Durante las horas de noche (1AM a 9AM) el bot "duerme"
5. Los 10 primeros eventos se hacen cada media hora, a partir de ahí cada hora. Cuando queden 4 jugadores o menos vuelven a ser cada media hora 
6. El juego solo acaba cuando quede un jugador

### Eventos

- ATAQUE: Un jugador le quita una vida a otro
- SUICIDIO: Un jugador se quita una vida a sí mismo
- RECUPERACIÓN: Un jugador recupera un punto de vida
- ALIANZA: Dos jugador se alían, por lo tanto, no se atacan hasta que sean los dos últimos jugadores. Sólo se puede tener una alianza con un jugador por lo que una alianza previa podría romperse en cualquier momento. Si un jugador muere, la alianza que tuviera también se rompe