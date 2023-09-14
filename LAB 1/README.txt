Integrantes:
    José Pinto - 202073559-K
    Ernesto Barria - 202073521-2

Instrucciones en Linux:
    - Abrir 3 terminales en el siguiente orden, en cada una de ellas ejecutar los siguientes comandos:
        Terminal 1: 
            go build connect4_server.go && ./connect4_server 

        Terminal 2:
            python3 intermediary_server.py

        Terminal 3:
            python3 client.py

Instrucciones en Windows:
    - Abrir 3 terminales en el siguiente orden, en cada una de ellas ejecutar los siguientes comandos:
        Terminal 1: 
            go build connect4_server.go && connect4_server.exe

        Terminal 2:
            python intermediary_server.py

        Terminal 3:
            python client.py

Instrucciones de juego:
    - El juego se inicia con el jugador 1, el cual debe ingresar la columna en la que desea colocar su ficha.
    - El juego termina cuando un jugador gana o cuando se llena el tablero (Empate).
    - Para volver a jugar, se debe ejecutar nuevamente las instrucciones de ejecución del juego.