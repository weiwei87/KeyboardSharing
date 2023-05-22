import ssl
import socket
import time
# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Generate an SSL context
context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="certificate.crt", keyfile="private.key")

# Bind the socket to a specific address and port
server_address = ('ubuntulaptop', 443)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)
print('Server is listening on {}:{}'.format(*server_address))

while True:
    # Wait for a client to connect
    print('Waiting for a connection...')
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))
    time.sleep(1)
    try:
        # Wrap the client socket in an SSL context
        ssl_socket = context.wrap_socket(client_socket, server_side=True)

        # Receive data from the client
        data = ssl_socket.recv(1024)
        print('Received data:', data.decode())

        # Send a response back to the client
        response = 'Hello, client!'
        ssl_socket.sendall(response.encode())

    finally:
        # Close the SSL socket
        ssl_socket.close()

