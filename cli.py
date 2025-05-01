import click
from dht_node import DHTNode
import json
import time
import socket

@click.group()
def cli():
    """Simple DHT CLI interface."""
    pass

@cli.command()
@click.option('--host', default='0.0.0.0', help='Host to bind to')
@click.option('--port', default=5000, help='Port to bind to')
@click.option('--bootstrap', help='Comma-separated list of bootstrap nodes (host:port)')
def start(host, port, bootstrap):
    """Start a new DHT node."""
    bootstrap_nodes = bootstrap.split(',') if bootstrap else []
    node = DHTNode(host, port, bootstrap_nodes)
    node.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        node.stop()

def _send_message(host: str, port: int, message: dict) -> dict:
    """Send a message to a DHT node and wait for response."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Send message
        sock.sendto(json.dumps(message).encode(), (host, port))
        
        # Set timeout for response
        sock.settimeout(5.0)
        
        # Wait for response
        data, _ = sock.recvfrom(4096)
        return json.loads(data.decode())
    finally:
        sock.close()

@cli.command()
@click.option('--host', required=True, help='Host of the DHT node')
@click.option('--port', required=True, type=int, help='Port of the DHT node')
@click.argument('key')
@click.argument('value')
def put(host, port, key, value):
    """Store a key-value pair in the DHT."""
    response = _send_message(host, port, {
        'type': 'store',
        'key': key,
        'value': value
    })
    
    if response.get('type') == 'store_ack':
        click.echo(f"Successfully stored {key}={value}")
    else:
        click.echo(f"Failed to store {key}={value}")

@cli.command()
@click.option('--host', required=True, help='Host of the DHT node')
@click.option('--port', required=True, type=int, help='Port of the DHT node')
@click.argument('key')
def get(host, port, key):
    """Retrieve a value from the DHT."""
    response = _send_message(host, port, {
        'type': 'get',
        'key': key
    })
    
    if response.get('type') == 'get_response':
        value = response.get('value')
        if value is None:
            click.echo(f"No value found for key: {key}")
        else:
            click.echo(f"Value for {key}: {value}")
    else:
        click.echo(f"Failed to retrieve value for key: {key}")

if __name__ == '__main__':
    cli() 