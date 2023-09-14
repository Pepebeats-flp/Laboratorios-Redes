package main

import (
	"fmt"
	"math/rand"
	"net"
	"strconv"
)

func game(ip string, port string, conn_che *net.UDPConn) {
	// Conectar con el servidor para recibir el tablero
	for {

		// Crear una dirección UDP en el puerto port
		addr, err := net.ResolveUDPAddr("udp", "localhost:"+port)
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

		// Recibir mensaje y guardar la respuesta en buffer
		buffer := make([]byte, 1024)
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error leyendo el mensaje:", err)
			return
		}
		fmt.Println("Recibido:", string(buffer[0:n]), "de", addr)
		request := string(buffer[0:n])

		// Verificamos si es una solicitud de terminar el juego
		if request == "Terminar" {
			// Respondemos con "OK,IP,PUERTO" si se pudo conectar
			response := "Terminar"
			_, err := conn.WriteToUDP([]byte(response), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
			break
		}

		// Verificamos si es una solicitud de jugar
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

			// Enviar random_port al cliente mediante UDP en puerto aleatorio
			random_port := rand.Intn(65535-8000) + 8000
			port = strconv.Itoa(random_port)

			// Mandar el puerto y la columna al cliente
			_, err := conn_che.WriteToUDP([]byte(bot_col_str+",localhost,"+port), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
		}
		// Cerrar la conexión
		defer conn.Close()
	}
}

func main() {
	// Creamos la dirección UDP en el puerto 12345
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

	// Recibir y mandar mensajes
	for {
		// Recibir mensaje y guardar la respuesta en buffer
		buffer := make([]byte, 1024)
		n, addr, err := conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error leyendo el mensaje:", err)
			return
		}
		fmt.Println("Recibido:", string(buffer[0:n]), "de", addr)
		request := string(buffer[0:n])
		// Verificamos si es una solicitud de inicio de juego
		if request == "Iniciar juego" {
			// Respondemos con "OK,IP,PUERTO" si se pudo conectar
			random_port := rand.Intn(65535-8000) + 8000
			random_port_str := strconv.Itoa(random_port)
			response := "Ok," + addr.IP.String() + "," + random_port_str
			_, err := conn.WriteToUDP([]byte(response), addr)
			if err != nil {
				fmt.Println("Error al enviar la respuesta:", err)
			}
			game(addr.IP.String(), random_port_str, conn)

			break
		}
	}
	// Cerrar la conexión
	defer conn.Close()
}
