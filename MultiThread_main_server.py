import queue
import threading
import ssl
import socket
import time
import pickle
from pynput import keyboard

# Create a shared queue
shared_queue = queue.Queue()
socketpool=set()

#keyboard operation
def on_key_press(key):
    print(f"Key pressed: {key}")
    shared_queue.put(key)

def on_key_release(key):
    print(f"Key released: {key}")

def senddata(data):
    for socket in socketpool:
        print(f"data is {data}")
        #        data1 = pickle.dump(data,open( "save.p", "wb" ))
        data1 = pickle.dumps(data) #bytes
        print(data1)
        hex1=data1.hex()
        socket.send(hex1.encode())

# Producer thread
def producer_thread():
    with keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()


# Consumer thread
def consumer_thread():

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Generate an SSL context
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="ssl/certificate.crt", keyfile="ssl/private.key")

    # Bind the socket to a specific address and port
    server_address = ('ubuntulaptop', 8080)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a client to connect
        print('Waiting for a connection...')
        client_socket, client_address = server_socket.accept()
        print('Accepted connection from {}:{}'.format(*client_address))

        #time.sleep(1)
            # Wrap the client socket in an SSL context
        ssl_socket = context.wrap_socket(client_socket, server_side=True)
        socketpool.add(ssl_socket)
        # Receive data from the client
        data = ssl_socket.recv(1024)
        print('Received data:', data.decode())

        # Send a response back to the client
        response = 'Hello, client!'
        ssl_socket.sendall(response.encode())
        while True:
            data = shared_queue.get()
            if data:
                # Consume the data
                try:
                    senddata(data)
                except:
                    print('error')
            # Close the SSL socket
                    ssl_socket.close()
                    socketpool.remove(ssl_socket)
                    break

                

        
        
        # Retrieve data from the queue


# Create and start the producer and consumer threads
producer = threading.Thread(target=producer_thread)
consumer = threading.Thread(target=consumer_thread)

producer.start()
consumer.start()
