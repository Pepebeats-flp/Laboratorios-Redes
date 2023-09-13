package main

import (
	"fmt"
	"math/rand"
	"net"
)

func handleUDPConnection(conn *net.UDPConn) {
	defer conn.Close()

	fmt.Println("Servidor escuchando en localhost:12345")

	// Buffer para recibir datos
	buffer := make([]byte, 1024)

	for {
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error al leer datos:", err)
			return
		}

		// Recibimos la solicitud inicial del cliente
		request := string(buffer[:n])
		fmt.Printf("Recibido desde %s: %s\n", addr, request)

		// Verificamos si es una solicitud de inicio de juego
		if request == "Iniciar juego" {
			// Respondemos con "OK,IP,PUERTO" si se pudo conectar
			response := "Ok," + addr.IP.String() + "," + "12346"
			_, err := conn.WriteToUDP([]byte(response), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
		} else {
			// Respondemos con "No,IP,PUERTO" si no se pudo conectar
			response := "No," + addr.IP.String() + "," + "12346"
			_, err := conn.WriteToUDP([]byte(response), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
		}
	}
}

// // Abrir otra conexi ́on UDP en un puerto aleatorio (entre 8000 y 65.535) cada vez que se pida una jugada
func handleUDPConnection2() {
	randomPort := rand.Intn(65535-8000) + 8000
	addr, err := net.ResolveUDPAddr("udp", "localhost:"+string(randomPort))
	if err != nil {
		fmt.Println("Error resolviendo la dirección:", err)
		return
	}
	// Crear una conexión UDP
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println("Error creando la conexión UDP:", err)
		return
	}
	// Manejar la conexión UDP en una función
	handleUDPConnection(conn)

	// Enviar una jugada al servidor
	conn.Write([]byte("Jugada"))

	// Cerrar la conexión
	defer conn.Close()

}

func main() {

	// Crear una dirección UDP en el puerto 12345
	addr, err := net.ResolveUDPAddr("udp", "localhost:12345")
	if err != nil {
		fmt.Println("Error resolviendo la dirección:", err)
		return
	}
	// Crear una conexión UDP
	conn, err := net.ListenUDP("udp", addr)
	if err != nil {
		fmt.Println("Error creando la conexión UDP:", err)
		return
	}
	// Manejar la conexión UDP en una función
	handleUDPConnection(conn)

	// Cerrar la conexión
	defer conn.Close()

}
