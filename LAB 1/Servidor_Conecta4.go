packge main

import (
	"net"
	"math/rand"
	"time"
	"fmt"
)

// Este nodo cumple el rol de BOT en la l´ogica del Jugador versus Computadora. Por lo tanto, 
// este nodo juega contra el Cliente ejecutando jugadas aleatorias hasta que se le indique el final del
// juego. Para esto, se deben satisfacer las siguientes tareas:

//• Abrir una conexi´on UDP para comunicarse con el Servidor Intermediario.
//• Abrir otra conexi´on UDP en un puerto aleatorio (entre 8000 y 65.535) cada vez que se pida una jugada.
//• Enviar mensajes al Servidor Intermediario y tambi´en recibir mensajes del mismo.
//• Debe terminar su ejecuci´on cuando se lo indique el Servidor Intermediario.
//• Informar de intercambios de mensajes dentro de su consola, junto con la apertura y cierre de puertos.

