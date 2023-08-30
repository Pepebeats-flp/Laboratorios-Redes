package main

import (
	"fmt"
	"math/rand"
	"net"
	"time"
)

func main() {
	intermediaryServerAddr := "intermediary_server_ip:intermediary_server_port"
	conn, err := net.Dial("udp", intermediaryServerAddr)
	if err != nil {
		fmt.Println("Error al conectar con el Servidor Intermediario:", err)
		return
	}
	defer conn.Close()

	fmt.Println("Conexión establecida con el Servidor Intermediario.")

	rand.Seed(time.Now().UnixNano())
	port := 8000 + rand.Intn(65535-8000)
	botAddr := fmt.Sprintf(":%d", port)

	botServerConn, err := net.ListenPacket("udp", botAddr)
	if err != nil {
		fmt.Println("Error al abrir el puerto UDP:", err)
		return
	}
	defer botServerConn.Close()

	fmt.Printf("Servidor Conecta4 BOT escuchando en el puerto %d.\n", port)

	buffer := make([]byte, 1024)

	for {
		n, addr, err := botServerConn.ReadFrom(buffer)
		if err != nil {
			fmt.Println("Error al leer desde el puerto UDP:", err)
			continue
		}

		message := string(buffer[:n])
		fmt.Printf("Mensaje recibido desde %s: %s\n", addr, message)

		// Implementa la lógica para generar una jugada aleatoria
		// y enviarla al Servidor Intermediario

		if message == "fin" {
			fmt.Println("Terminando la ejecución.")
			break
		}
	}
}
