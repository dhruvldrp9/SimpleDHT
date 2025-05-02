#!/usr/bin/env python3
"""
Advanced example of SimpleDHT package for distributed storage
"""
from simpledht import DHTNode
import threading
import time
import random
import string

def generate_random_data(size=10):
    """Generate random key-value pairs"""
    return {
        ''.join(random.choices(string.ascii_letters, k=5)): 
        ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        for _ in range(size)
    }

class StorageNode:
    def __init__(self, port, bootstrap_node=None):
        self.node = DHTNode(host='0.0.0.0', port=port)
        self.bootstrap_node = bootstrap_node
        self.running = False

    def start(self):
        """Start the node and connect to bootstrap node if provided"""
        self.node.start()
        self.running = True
        
        if self.bootstrap_node:
            self.node.bootstrap(self.bootstrap_node)
            print(f"Node on port {self.node.port} connected to bootstrap node {self.bootstrap_node}")
        
        # Start background tasks
        threading.Thread(target=self._background_tasks, daemon=True).start()

    def stop(self):
        """Stop the node"""
        self.running = False
        self.node.stop()

    def _background_tasks(self):
        """Background tasks for the node"""
        while self.running:
            # Periodically check node health
            self._check_health()
            time.sleep(5)

    def _check_health(self):
        """Check node health and log status"""
        print(f"Node {self.node.port} is running with {len(self.node.peers)} peers")

def main():
    # Create a network of 3 nodes
    nodes = []
    
    # Start the first node (bootstrap node)
    node1 = StorageNode(5000)
    node1.start()
    nodes.append(node1)
    print("Bootstrap node started on port 5000")

    # Start two more nodes and connect them to the bootstrap node
    for port in [5001, 5002]:
        node = StorageNode(port, 'localhost:5000')
        node.start()
        nodes.append(node)
        print(f"Node started on port {port}")

    try:
        # Store some random data
        data = generate_random_data(5)
        for key, value in data.items():
            # Store on random node
            random_node = random.choice(nodes)
            random_node.node.put(key, value)
            print(f"Stored {key}={value} on node {random_node.node.port}")

        # Wait for replication
        time.sleep(2)

        # Verify data is accessible from all nodes
        for node in nodes:
            print(f"\nVerifying data on node {node.node.port}:")
            for key in data:
                value = node.node.get(key)
                print(f"  {key}: {value}")

        # Keep running to demonstrate background tasks
        print("\nNodes are running with background tasks. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down nodes...")
        for node in nodes:
            node.stop()

if __name__ == '__main__':
    main() 