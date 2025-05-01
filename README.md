# Simple DHT

A simple Distributed Hash Table (DHT) implementation that allows nodes to connect across different regions using IP addresses.

## Features

- Node discovery and routing
- Key-value storage across the network
- Support for multiple nodes in different regions
- Simple CLI interface

## Installation

1. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting a Node

To start a new DHT node:
```bash
python cli.py start --host 0.0.0.0 --port 5000
```

To start a node and connect to existing nodes:
```bash
python cli.py start --host 0.0.0.0 --port 5001 --bootstrap "192.168.1.100:5000,192.168.1.101:5000"
```

### Storing Data

To store a key-value pair:
```bash
python cli.py put --host 192.168.1.100 --port 5000 mykey "my value"
```

### Retrieving Data

To retrieve a value:
```bash
python cli.py get --host 192.168.1.100 --port 5000 mykey
```

## Architecture

The DHT implementation uses:
- UDP sockets for communication
- SHA-256 for node ID generation
- Simple key-based routing
- Bootstrap nodes for network discovery

## Security Considerations

- This is a basic implementation and should not be used in production without additional security measures
- Consider adding encryption for data in transit
- Implement proper authentication for node joining
- Add rate limiting to prevent abuse
