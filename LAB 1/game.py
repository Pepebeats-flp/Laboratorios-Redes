import socket


def conex_inter():
    conex_cliente()
    return True

def game():
    print("'juego xd ... '" )
    return True





# Main
print("- - - - - - - - Bienvenido al Juego - - - - - - - -")
while True:
    print("1- Jugar")
    print("2- Salir")
    opcion = int(input())
    if opcion == 1:
        print("Conectando con el servidor intermediario")
        if conex_inter() == True:
            print("respuesta de disponibilidad: OK")
            print("- - - - - - - - Comienza el Juego - - - - - - - -")
            game()
            print("- - - - - - - - ¿Quieres jugar de nuevo? - - - - - - - -")
        else:
            print("respuesta de disponibilidad: NO")
            print("- - - - - - - - Intenta de nuevo - - - - - - - -")
    elif opcion == 2:
        print("- - - - - - - - Saliendo - - - - - - - -")
        break
    else:
        print("- - - - - - - - Opcion invalida - - - - - - - -")

    



