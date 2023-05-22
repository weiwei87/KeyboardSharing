import ssl
import socket
from pynput.keyboard import Key, Controller
import pickle
import time


# Create an SSL context
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

# Set the hostname or IP address of the server
hostname = 'ubuntulaptop'

keyboard = Controller()

def handledata(data):
#favorite_color = pickle.load( open( "save.p", "rb" ) )
    data = bytes.fromhex(data)
    data = pickle.loads(data)
    print(f'received {data}')

    '''try:
        data = data.char
    except AttributeError:
        data = 'Key.' + data.name
    print(data)'''
    time.sleep(1)
    keyboard.press(data)

'''    if hasattr(data, 'char'):
        # Handle printable keys
        print(f"Key pressed: {key.char}")
        keyboard.press(data.char)
    else:
        # Handle non-printable keys
        print(f"Key pressed: {key.name}")
        keyboard.press(data.name)    '''

# Configure the SSL context to trust the self-signed certificate
#context.load_verify_locations(cafile="server.crt")

# Connect to the server using SSL/TLS
with socket.create_connection((hostname, 8080)) as sock:
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
        try:
            while True:
                data = ssock.recv(1024)
                if not data:
                    # No more data, break the loop
                    break
                
                handledata(data.decode())
                
        except:
            print('error')
            
        finally:
            ssock.close()
     
     
     
     
