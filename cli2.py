import ssl
import socket

# Create an SSL context
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Set the hostname or IP address of the server
hostname = 'ubuntulaptop'

# Configure the SSL context to trust the self-signed certificate
#context.load_verify_locations(cafile="server.crt")

# Connect to the server using SSL/TLS
with socket.create_connection((hostname, 443)) as sock:
    # Wrap the socket with SSL/TLS
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        # Receive the server's certificate
        server_cert = ssock.getpeercert()

        # Verify the server's certificate (optional)
        # You may add custom certificate verification logic here
        # For example, checking the certificate's subject, expiration, etc.

        # Send data to the server
        message = 'Hello, server!'
        ssock.sendall(message.encode())

        # Receive the response from the server
        response = ssock.recv(1024)

# Print the response
print('Response from server:', response.decode())

