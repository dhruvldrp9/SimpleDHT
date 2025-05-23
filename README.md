# Distributed Hash Table (DHT) Implementation

A Python-based Distributed Hash Table implementation that allows nodes to connect across different networks using IP addresses. This implementation supports key-value storage and retrieval across multiple nodes.

## Features

- Cross-network node communication
- Key-value storage and retrieval
- Automatic node discovery
- Data replication between nodes
- Data synchronization when joining the network
- Reliable bootstrapping with retry mechanism
- Simple CLI interface
- Public IP detection
- Local network support
- Python library interface for programmatic use

## Installation

### From PyPI (Recommended)

```bash
pip install simpledht
```

### From Source

1. Clone the repository:
```bash
git clone https://github.com/dhruvldrp9/SimpleDHT
cd SimpleDHT
```

2. Create and activate a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

## Usage

### As a Python Library

The package can be used programmatically in your Python code:

```python
from simpledht import DHTNode

# Create and start a node
node = DHTNode(host='0.0.0.0', port=5000)
node.start()

# Store data
node.put('mykey', 'myvalue')

# Retrieve data
value = node.get('mykey')

# Connect to another node
node.bootstrap('other_node_ip:5000')

# Stop the node when done
node.stop()
```

See the `examples/` directory for more detailed usage examples:
- `basic_usage.py`: Simple example of creating and connecting nodes
- `distributed_storage.py`: Advanced example showing distributed storage with multiple nodes

### Command Line Interface

#### Starting a Node

To start a new DHT node:

```bash
python -m simpledht.cli start --host 0.0.0.0 --port 5000
```

To start a node and connect to existing nodes:

```bash
python -m simpledht.cli start --host 0.0.0.0 --port 5001 --bootstrap "PUBLIC_IP:5000"
```

#### Storing Data

To store a key-value pair:

```bash
python -m simpledht.cli put --host PUBLIC_IP --port 5000 mykey "my value"
```

#### Retrieving Data

```bash
python -m simpledht.cli get --host PUBLIC_IP --port 5000 mykey
```

### Cross-Network Example

1. Start Node 1 (First network):
```bash
python -m simpledht.cli start --host 0.0.0.0 --port 5000
```

2. Start Node 2 (Second network):
```bash
python -m simpledht.cli start --host 0.0.0.0 --port 5000 --bootstrap "NODE1_PUBLIC_IP:5000"
```

3. Store and retrieve data:
```bash
# Store on Node 1
python -m simpledht.cli put --host NODE1_PUBLIC_IP --port 5000 test_key "test_value"

# Retrieve from Node 2
python -m simpledht.cli get --host NODE2_PUBLIC_IP --port 5000 test_key
```

## Network Configuration

### Firewall Setup

Ensure the UDP port (default: 5000) is open in your firewall:

```bash
# For UFW (Ubuntu)
sudo ufw allow 5000/udp

# For iptables
sudo iptables -A INPUT -p udp --dport 5000 -j ACCEPT
```

### Port Forwarding

If your node is behind a NAT router:
1. Access your router's admin interface
2. Set up port forwarding for UDP port 5000
3. Forward to your node's local IP address

## New Features in Version 0.1.3

- **Improved Bootstrap Mechanism**: Added retry logic for more reliable connections across networks
- **Data Synchronization**: Nodes automatically sync data when joining the network
- **Enhanced Error Handling**: Better handling of network timeouts and connection issues
- **Full Data Replication**: All nodes maintain a complete copy of the data for redundancy
- **Alternative Command Method**: Added support for running via `python -m simpledht.cli`

## Troubleshooting

### Common Issues

1. **Connection Timeout**
   - Check if the target node is running
   - Verify firewall settings
   - Ensure port forwarding is configured correctly
   - Try increasing the timeout: `--timeout 10`

2. **Address Already in Use**
   - The port is already being used by another process
   - Try a different port number
   - Check running processes: `netstat -tuln | grep 5000`

3. **No Response from Node**
   - Verify the node is running
   - Check network connectivity: `ping NODE_IP`
   - Test port connectivity: `nc -vzu NODE_IP 5000`

### Error Messages

- `Failed to bootstrap with IP:PORT`: Invalid bootstrap node format
- `No response received`: Node is not responding
- `Address already in use`: Port conflict
- `Failed to get public IP`: Network connectivity issue
- `Connection attempt X/3 timed out, retrying...`: Network latency or connectivity issues
- `simpledht: command not found`: The command-line tool is not in your PATH. Use the Python module directly: `python -m simpledht.cli`

## Architecture

The DHT implementation uses:
- UDP sockets for communication
- SHA-256 for node ID generation
- Automatic public IP detection
- Data replication between nodes
- Bootstrap nodes for network discovery
- Retry mechanism for reliable connections

## Security Considerations

- This is a basic implementation and should not be used in production without additional security measures
- Consider adding:
  - Encryption for data in transit
  - Authentication for node joining
  - Rate limiting to prevent abuse
  - Input validation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
