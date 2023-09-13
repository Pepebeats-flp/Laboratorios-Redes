package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
)

func handleUDPConnection(conn *net.UDPConn) {
	defer conn.Close()

	fmt.Println("Servidor escuchando en " + conn.LocalAddr().String())

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
		}
		if request == "Terminar" {
			// Respondemos con "OK,IP,PUERTO" si se pudo conectar
			response := "Ok," + addr.IP.String() + "," + "12346"
			_, err := conn.WriteToUDP([]byte(response), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
		}
		if len(request) == 6 {
			disponibles := []int{}
			// binario con las columnas disponibles para jugar
			for pos, char := range request {
				if char == '1' {
					// agregar a una lista de columnas disponibles
					disponibles = append(disponibles, pos+1)
				}
			}

			// Seleccionar una columna disponible al azar
			bot_i := rand.Intn(len(disponibles))
			bot_col := disponibles[bot_i]

			// Convertir a string
			bot_col_str := strconv.Itoa(bot_col)

			// Enviar random_port al cliente medianrte UDP en puerto 12346
			random_port := rand.Intn(65535-8000) + 8000
			random_port_str := strconv.Itoa(random_port)

			// Crear una dirección UDP en el puerto random_port
			addr, err := net.ResolveUDPAddr("udp", "localhost:"+random_port_str)

			// Crear una conexión UDP
			conn, err := net.ListenUDP("udp", addr)
			if err != nil {
				fmt.Println("Error creando la conexión UDP:", err)
				return
			}

			// Cerrar la conexión
			defer conn.Close()

			// Enviar la columna seleccionada
			_, err = conn.WriteToUDP([]byte(bot_col_str), addr)
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
