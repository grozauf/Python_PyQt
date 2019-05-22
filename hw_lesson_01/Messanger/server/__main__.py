from argparse import ArgumentParser
import socket
import datetime
import logging
import select
import threading
import jim
import settings
from routes import resolve, get_server_routes
from protocol import (
    validate_request, make_response,
    make_400, make_404
)

from handlers import handle_request


def get_response_msg():
    msg = {
        "response": 200,
        "alert": "Необязательное сообщение/уведомление"
    }
    return jim.pack(msg)


def read_client_data(client, requests, buffersize):
    try:
        b_request = client.recv(buffersize)
    except ConnectionResetError:
        b_request = b''
    if b_request != b'':
        requests.append(b_request)


def write_client_data(client, response):
    client.send(response)


host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)

parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address')
parser.add_argument('-p', '--port', type=int, help='Sets port')

args = parser.parse_args()

if args.addr:
    host = args.addr
if args.port:
    port = args.port

handler = logging.FileHandler('main.log', encoding=settings.ENCODING)
error_handler = logging.FileHandler('error.log', encoding=settings.ENCODING)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        handler,
        error_handler,
        logging.StreamHandler(),
    ]
)


def main():

    requests = []
    connections = []

    try:
        sock = socket.socket()
        sock.bind((host, port))
        sock.settimeout(0)
        sock.listen(5)
        logging.info(f'Server started with {host}:{port}')
        while True:
            try:
                client, address = sock.accept()
                logging.info(f'Client detected {address}')
                connections.append(client)
            except Exception:
                pass

            if connections != []:
                rlist, wlist, xlist = select.select(
                    connections, connections, connections, 0
                )

                for r_client in rlist:
                    thread = threading.Thread(
                        target=read_client_data,
                        args=(r_client, requests, settings.BUFFERSIZE)
                    )
                    thread.start()

                if requests:
                    b_request = requests.pop()
                    print(b_request)

                    if b_request != b'':
                        b_response = handle_request(b_request)

                        for w_client in wlist:
                            thread = threading.Thread(
                                target=write_client_data,
                                args=(w_client, b_response)
                            )
                            thread.start()

    except KeyboardInterrupt:
        logging.info('Server  closed')


main()
