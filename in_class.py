import socket
import signal
import sys
import threading
import re
import json

# Define the server's IP address and port
HOST = '127.0.0.1'  # IP address to bind to (localhost)
PORT = 8081         # Port to listen on

# Create a socket that uses IPv4 and TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)  # Increased backlog for multiple simultaneous connections
print(f"Server is listening on {HOST}:{PORT}")

# Function to handle client requests
def handle_request(client_socket):
    # Receive and print the client's request data
    request_data = client_socket.recv(1024).decode('utf-8')
    print(f"Received Request:\n{request_data}")

    # Parse the request to get the HTTP method and path
    request_lines = request_data.split('\n')
    request_line = request_lines[0].strip().split()
    method = request_line[0]
    path = request_line[1]

    # Initialize the response content and status code
    response_content = ''
    status_code = 200

    # Define a simple routing mechanism
    products = re.compile("/product/[0-9]")
    if path == '/':
        response_content = 'This is the home page you are welcome!'
    elif path == '/about':
        response_content = 'This is the About page.'
    elif path == '/contacts':
        response_content = 'Contacts: +373666666\n Location: Somewhere in Moldova'
    elif path == '/products':
        with open("products.json", "r") as file:
            json_data = json.load(file)
        products = json_data["products"]
        product_nr = 1
        for product in products:
            response_content += "<a href=\"/product/" + str(product_nr) + "\">" + "product: " + str(product_nr) + "</a><br>"
            response_content += "<ul>"
            for key, value in product.items():
                response_content += "<li>" + str(key) + ": " + str(value) + "</li><br>"
            response_content += "</ul>"
            response_content += "<br>"
            product_nr += 1
    elif products.match(path):
        number = str(path).replace("/product/","")
        with open("products.json", "r") as file:
            json_data = json.load(file)
        products = json_data["products"]
        product_nr = 1
        for product in products:
            if int(number) == product_nr:
                response_content += "product: " + str(product_nr) + "<br>"
                response_content += "<ul>"
                for key, value in product.items():
                    response_content += "<li>" + str(key) + ": " + str(value) + "</li><br>"
                response_content += "</ul>"
                response_content += "<br>"
            product_nr += 1
        if (len(response_content) == 0):
            response_content = '404 Not Found'
            status_code = 404
    else:
        response_content = '404 Not Found'
        status_code = 404

    # Prepare the HTTP response
    response = f'HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_content}'
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()

# Function to handle Ctrl+C and other signals
def signal_handler(sig, frame):
    print("\nShutting down the server...")
    server_socket.close()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

while True:
    # Accept incoming client connections
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()