from flask import Flask, request, jsonify
import requests

# Create a flask app
app = Flask(__name__)

# Define main route
@app.route('/')
def main():
    return 'Welcome!'

# Define a route for the "/fibonacci" path
@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    # Extract query parameters
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = int(request.args.get('as_port')) # convert as_port into an int
    
    # Make a DNS query to the Authoriative Server (AS) to resolve the hostname
    as_query = f"TYPE=A\nNAME={hostname}"
    as_response = requests.get(f'http://{as_ip}:{as_port}/query?{as_query}')

    if as_response.status_code == 200:
        # If the DNS query is successful, extract the resolved IP from response
        ip = as_response.text.strip() # strip any leading or trailing whitespace
    else:
        # Handle the case when DNS resolution failed 
        return "DNS resolution failed", 400

    # Make a request to the Fibonacci Server using the resolved IP
    fp_response = requests.get(f'http://{ip}:{fs_port}/fibonacci?number={number}')

    # Process the response and return the result
    result = fp_response.text

    return result
    

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)





