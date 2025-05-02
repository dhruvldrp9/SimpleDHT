#!/usr/bin/env python3
"""
Basic usage example of SimpleDHT package
"""
from simpledht import DHTNode
import time

def main():
    # Create and start the first node
    node1 = DHTNode(host='0.0.0.0', port=5000)
    node1.start()
    print("Node 1 started on port 5000")

    # Create and start the second node
    node2 = DHTNode(host='0.0.0.0', port=5001)
    node2.start()
    print("Node 2 started on port 5001")

    # Connect node2 to node1
    # node2.bootstrap('localhost:5000')
    # print("Node 2 connected to Node 1")

    # Store some data on node1
    node1.put('test_key', 'test_value')
    print("Stored 'test_value' with key 'test_key' on Node 1")

    # Wait for replication
    time.sleep(1)

    # Retrieve data from node2
    value = node1.get('test_key')
    print(f"Retrieved value from Node 2: {value}")

    # Clean up
    node1.stop()
    node2.stop()

if __name__ == '__main__':
    main() 