import socket


def start_web_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 5000))
    server.listen()

    try:
        while True:
            print('Server waiting...')
            client, client_addr = server.accept()
            data = client.recv(4096).decode()
            print(f'Client data: {data}')
            content = load_page_from_request(data)
            client.send(content)
            client.shutdown(socket.SHUT_WR)
    except KeyboardInterrupt:
        server.close()
        print('Shutdown server.')


def load_page_from_request(request):
    try:
        path = request.split(' ')[1]
    except IndexError:
        path = '/'

    if path == '/':
        path = '/home.html'

    try:
        with open('views' + path, 'rb') as file:
            response = file.read()

        return HEADERS.encode() + response
    except FileNotFoundError:
        with open('views' + '/404.html', 'rb') as fl_404:
            response_404 = fl_404.read()
        return HEADERS_404.encode() + response_404


HEADERS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
HEADERS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'

if __name__ == '__main__':
    start_web_server()
