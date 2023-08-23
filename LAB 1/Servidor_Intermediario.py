'''Este nodo cumple el rol de comunicar el Cliente con el Servidor Conecta4. Para esto, se deben satisfacer las siguientes tareas:
• Mantener una conexion TCP con el Cliente.
• Conectarse, cuando sea requerido, con el Servidor Gato mediante una conexion UDP.
• Responder al Cliente con el mensaje que recibe del Servidor Conecta4.
• Este debe procesar el turno revisando posibles ganadores y enviar el resultado junto con la jugada al Cliente.
• Alertar al Servidor Conecta4 del termino del juego para que, este pueda terminar su ejecucion
• Debe terminar su ejecucion cuando el Cliente le indique el termino del juego (No sin antes igualmente notificar al Servidor Conecta4).
• Informar sobre el intercambio de mensajes entre los demas nodos. '''


import socket






