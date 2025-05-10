#!/usr/bin/env python3
"""
Cross-network example for SimpleDHT package (version 0.1.2+)

This example demonstrates how to connect nodes across different networks
using public IP addresses and how the data synchronization works.

To run this example:
1. Run this script on two different machines (or networks)
2. On the first machine, it will start as a bootstrap node
3. On the second machine, provide the public IP of the first machine
"""
from simpledht import DHTNode
import time
import sys
import random
import string
import argparse

def generate_random_data(size=5):
    """Generate random key-value pairs"""
    return {
        ''.join(random.choices(string.ascii_letters, k=5)): 
        ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        for _ in range(size)
    }

def main():
    parser = argparse.ArgumentParser(description='Cross-network DHT example')
    parser.add_argument('--bootstrap', help='Bootstrap node address (IP:PORT)')
    parser.add_argument('--port', type=int, default=5000, help='Port to use')
    args = parser.parse_args()
    
    # Create a node
    node = DHTNode(host='0.0.0.0', port=args.port)
    node.start()
    
    print(f"Node started with ID: {node.id}")
    print(f"Public IP: {node.public_ip}")
    print(f"Local IPs: {', '.join(node.local_ips)}")
    
    # If bootstrap address is provided, connect to it
    if args.bootstrap:
        print(f"Connecting to bootstrap node at {args.bootstrap}")
        success = node.bootstrap(args.bootstrap)
        if success:
            print("Successfully connected to bootstrap node")
            print(f"Routing table: {len(node.routing_table)} entries")
            
            # Wait a moment for data sync
            print("Waiting for data synchronization...")
            time.sleep(2)
            
            # Check if we received any data
            if node.data:
                print(f"Received {len(node.data)} key-value pairs from the network:")
                for key, value in node.data.items():
                    print(f"  {key}: {value}")
            else:
                print("No data received from the network")
        else:
            print("Failed to connect to bootstrap node")
            sys.exit(1)
    else:
        print("Running as a bootstrap node")
        
        # Generate and store some random data
        data = generate_random_data()
        print("\nStoring random data:")
        for key, value in data.items():
            node.put(key, value)
            print(f"  Stored {key}: {value}")
    
    try:
        print("\nNode is running. Press Ctrl+C to stop.")
        while True:
            cmd = input("\nEnter command (put/get/info/quit): ").strip().lower()
            
            if cmd == 'quit':
                break
            elif cmd == 'put':
                key = input("Enter key: ").strip()
                value = input("Enter value: ").strip()
                node.put(key, value)
                print(f"Stored {key}: {value}")
            elif cmd == 'get':
                key = input("Enter key: ").strip()
                value = node.get(key)
                if value:
                    print(f"Value for {key}: {value}")
                else:
                    print(f"No value found for key: {key}")
            elif cmd == 'info':
                print(f"Node ID: {node.id}")
                print(f"Public IP: {node.public_ip}")
                print(f"Connected peers: {len(node.routing_table) - 1}")  # Exclude self
                print(f"Stored key-value pairs: {len(node.data)}")
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        print("\nStopping node...")
    finally:
        node.stop()
        print("Node stopped.")

if __name__ == '__main__':
    main() 