from flask import Flask, request, jsonify
import socket
import requests

# Create a flask app
app = Flask(__name__)

registered_server = {}


######################################################################################
########## Send a UDP registration request to the Authoritative Server (AS) ##########
######################################################################################
def register_with_auth_server(hostname, ip, as_ip, as_port):
    # Send a UDP registration request to the Authoritative Server (AS)
    regist_data = f"HTTP/1.1 PUT /register\r\n"
    regist_data += f"Host: {as_ip}:{as_port}\r\n"
    regist_data += f"Content-Length: {len(f'TYPE=A NAME={hostname} VALUE={ip} TTL=10')}\r\n"
    regist_data += f"Content-Type: application/json\r\n\r\n"
    regist_data += f"TYPE=A NAME={hostname} VALUE={ip} TTL=10"

    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_address = (as_ip, as_port)
    
    print(f"Sending registration data to AS server at {as_address}: {regist_data}")  # Debugging line
    
    as_socket.sendto(regist_data.encode(), as_address)
    as_socket.close()


############################################################################
########## Register the Server  with the Authoriative Server (AS) ##########
############################################################################
@app.route('/register', methods = ['PUT'])
def register():
    data = request.get_json()
    hostname = data['hostname']
    ip = data['ip']
    as_ip = data['as_ip']
    as_port = int(data['as_port'])

    # Register the server with the Authoriative Server (AS)
    registered_server[hostname] = {
        'ip': ip,
        'as_ip': as_ip,
        'as_port': as_port
    }

    # Register with the AS
    register_with_auth_server(hostname, ip, as_ip, as_port)

    return "Server registered successfully", 201



#########################################
########## Calculate Fibonacci ##########
#########################################
@app.route('/fibonacci', methods=['GET'])
def calculate_number():
    number = request.args.get('number')

    if number.isdigit() == False: # if number is not a digit
        return "Invalid input", 400
    
    number = int(number)
    if number < 0:
        return "Invalid number", 400
    elif number == 1:
        return "1", 200
    
    a, b = 0, 1
    for _ in range(2, number+1):
        a, b = b, a + b
    
    return str(b), 200


if __name__ == '__main__':
    app.run(port = 9090)
