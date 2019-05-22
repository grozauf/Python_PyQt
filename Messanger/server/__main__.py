from argparse import ArgumentParser
import socket
import datetime
import logging
import select
import threading
import jim
import settings
import dis
from routes import resolve, get_server_routes
from protocol import (
    validate_request, make_response,
    make_400, make_404
)

from handlers import handle_request

class ServerVerifier(type):

    def __init__(self, clsname, bases, clsdict):
        self.verify_class(clsname, clsdict)
        type.__init__(self, clsname, bases, clsdict)

    def verify_class(self, clsname, clsdict):

        socket_argval = None
        for key, value in clsdict.items():
            assert not isinstance(value, socket.socket), 'Creating socket in class level is forbidden'

            instructions_list = dis.get_instructions(value)
            for instruction in instructions_list:
                if instruction.argval == 'socket' and instruction.opname == 'LOAD_GLOBAL':
                    while instruction.opname != 'STORE_ATTR':
                        instruction = next(instructions_list)
                        if instruction.opname == 'LOAD_ATTR' and instruction.arg == 2:
                            assert instruction.argval == 'SOCK_STREAM', 'Only SOCK_STREAM sockets is available'
                    socket_argval = instruction.argval

        if socket_argval:
            for key, value in clsdict.items():
                forbidden_procs = ['connect']
                instructions_list = dis.get_instructions(value)
                for instruction in instructions_list:
                    if instruction.argval == socket_argval:
                        next_instruction = next(instructions_list)
                        assert not (next_instruction.argval in forbidden_procs and
                                    next_instruction.opname == 'LOAD_ATTR'), \
                            f"{clsname} has forbidden method {next_instruction.argval}"


class PortDescriptor:

    def __init__(self):
        self._value = 7777

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if type(value) is not int:
            raise TypeError('Value must be integer')
        if not value >= 0:
            raise ValueError('Port number must be => 0')
        self._value = value


class Server(metaclass=ServerVerifier):
    def __init__(self, host, port):
        self.host = host
        self.port = PortDescriptor()
        self.port = port
        self.sock = None

    def make_listen(self):
        self.sock = socket.socket()
        self.sock.bind((self.host, self.port))
        self.sock.settimeout(0)
        self.sock.listen(5)
        logging.info(f'Server started with {self.host}:{self.port}')

    def read_client_data(self, client, requests, buffersize):
        b_request = client.recv(buffersize)
        requests.append(b_request)

    def write_client_data(self, client, response):
        client.send(response)

    def run_event_loop(self):
        requests = []
        connections = []

        while True:
            try:
                client, address = self.sock.accept()
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
                        target=self.read_client_data,
                        args=(r_client, requests, settings.BUFFERSIZE)
                    )
                    thread.start()

                if requests:
                    b_request = requests.pop()
                    b_response = handle_request(b_request)

                    for w_client in wlist:
                        thread = threading.Thread(
                            target=self.write_client_data,
                            args=(w_client, b_response)
                        )
                        thread.start()



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

    serverObj = Server(host, port)
    try:
        serverObj.make_listen()
        serverObj.run_event_loop()
    except KeyboardInterrupt:
        logging.info('Server  closed')


main()
