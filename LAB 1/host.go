package main

import (
    "fmt"
    "net"
    "math/rand"
    "time"
)

func main() {
    // Generar un número de puerto aleatorio entre 8000 y 65535
    rand.Seed(time.Now().UnixNano())
    minPort := 8000
    maxPort := 65535
    port := rand.Intn(maxPort-minPort+1) + minPort

    // Crea una dirección UDP con el puerto aleatorio
    udpAddress, err := net.ResolveUDPAddr("udp", fmt.Sprintf(":%d", port))
    if err != nil {
        fmt.Println("Error resolviendo la dirección UDP:", err)
        return
    }

    // Crea una conexión UDP
    udpConn, err := net.ListenUDP("udp", udpAddress)
    if err != nil {
        fmt.Println("Error al iniciar la conexión UDP:", err)
        return
    }
    defer udpConn.Close()

    fmt.Printf("Servidor UDP escuchando en el puerto aleatorio %d\n", port)

    // Buffer para almacenar datos recibidos
    buffer := make([]byte, 1024)

    for {
        // Leer datos UDP
        n, addr, err := udpConn.ReadFromUDP(buffer)
        if err != nil {
            fmt.Println("Error al leer datos UDP:", err)
            return
        }

        // Procesar los datos recibidos
        data := buffer[:n]
        fmt.Printf("Recibido de %s: %s\n", addr, data)

		// Enviar una respuesta al cliente
        response := []byte("OK")
        _, err = udpConn.WriteToUDP(response, addr)
        if err != nil {
			response := []byte("NO")
			_, err = udpConn.WriteToUDP(response, addr)
            fmt.Println("Error al enviar la respuesta UDP:", err)
        }
    }
}