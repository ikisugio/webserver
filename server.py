import socket

def parse_request(request):
    lines = request.split('\r\n')
    meta = lines[0].split(' ')
    method = path = None  # Initialize to None
    if len(meta) == 3:
        method, path, _ = meta
    elif len(meta) == 2:
        method, path = meta
    else:
        print("Received invalid request:")
        print(request)
        return None, None, None
    headers = {}
    for line in lines[1:]:
        if line:
            key, value = line.split(': ', 1)
            headers[key] = value
    return method, path, headers

def generate_response(status_code, body, content_type='text/html'):
    response = f"HTTP/1.1 {status_code}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(body)}\r\n"
    response += "\r\n"
    response += body
    return response

def handle_request(client_socket):
    request = client_socket.recv(4096).decode('utf-8')
    method, path, headers = parse_request(request)
    if method is None or path is None:
        print("Failed to parse request, closing connection")
        # client_socket.close()
        return None

    method, path, headers = parse_request(request)
    print(f"Received request: {method} {path}")

    if path == '/':
        content = "Hello, World!"
        response = generate_response("200 OK AHOTARE", content)
    else:
        content = "404 Not Found"
        response = generate_response("404 NOT ☠FOUND BOKE KASU", content, content_type='text/plain')

    client_socket.sendall(response.encode('utf-8'))
    client_socket.close()


def main():
    host = '127.0.0.1'
    port = 8081

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is listening on http://{host}:{port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(
                f"Accepted connection from {client_address}"
            )
            handle_request(client_socket)
    except KeyboardInterrupt:
        print("Server is shutting down come by aiueo700.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
