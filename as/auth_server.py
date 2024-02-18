import socket
import json

# Create UDP Socket
as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

as_ip = "10.18.135.90"
as_port = 53533

as_socket.bind((as_ip, as_port))

dns_DB = {} # create a DNS database 

while True:
    data, address = as_socket.recvfrom(1024)
    query = data.decode("utf-8")
    print(f"Received data from {address}:{query}")

    lines = query.strip().split('\n')

    if len(lines) > 2:
        _, dns_type, dns_name, dns_value, dns_ttl = [line.strip() for line in lines[:4]]

        if dns_type == "TYPE=A" and dns_name and dns_value and dns_ttl:
            dns_DB[dns_name] = (dns_value, int(dns_ttl))
        else:
            response = "HTTP/1.1 201 Created\r\n\r\n"

    else:
        query_type, query_name = [line.strip() for line in lines]
        if query_type == "TYPE=A" and query_name:
            if query_name in dns_DB:
                ip, ttl = dns_DB[query_name]
                response = f"TYPE=A\nNAME={query_name}\nVALUE={ip} TTL={ttl}\n"
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            response = "HTTP/1.1 400 Bad Request\r\n\r\n"


    as_socket.sendto(response.encode(), address)
    print(f"Sent Response to {address}:{response}")