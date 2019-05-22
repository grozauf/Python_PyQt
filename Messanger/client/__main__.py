from argparse import ArgumentParser
import socket
import datetime
import logging
import jim
import settings
import dis

class ClientVerifier(type):

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
                forbidden_procs = ['listen', 'accept']
                instructions_list = dis.get_instructions(value)
                for instruction in instructions_list:
                    if instruction.argval == socket_argval:
                        next_instruction = next(instructions_list)
                        assert not (next_instruction.argval in forbidden_procs and
                                    next_instruction.opname == 'LOAD_ATTR'), \
                            f"{clsname} have forbidden method {next_instruction.argval}"


class Client(metaclass=ClientVerifier):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None

    def make_connection(self):
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        logger.info(f'Client started with {self.host}:{self.port}')
        print(f'Client started with {self.host}:{self.port}')

    def get_presence_msg(self, action, data):
        time = datetime.datetime.now()
        msg = {
            "action": action,
            "time": time.isoformat(),
            "user": {
                    "account_name":  "anonim",
                    "status":      "Yep, I am here!"
            },
            "data": data
        }

        return jim.pack(msg)

    def send_request(self):
        while True:
            action = input('Enter action to send:')
            data = input('Enter data to send:')

            msg = self.get_presence_msg(action, data)
            self.sock.sendall(msg)

    def recv_response(self):
        while True:
            response = self.sock.recv(settings.BUFFERSIZE)
            response = jim.unpack(response)
            logger.info(f'Got next response from server: {response}')
            print(f'Got next response from server: {response}')


host = getattr(settings, 'HOST', '127.0.0.1')
port = getattr(settings, 'PORT', 7777)

parser = ArgumentParser()
parser.add_argument('-a', '--addr', type=str, help='Sets ip address')
parser.add_argument('-p', '--port', type=int, help='Sets port')
parser.add_argument('-m', '--mode', type=str, default='w')

args = parser.parse_args()

if args.addr:
    host = args.addr
if args.port:
    port = args.port

logger = logging.getLogger('main')
handler = logging.FileHandler('client.log', encoding=settings.ENCODING)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

try:

    clientObj = Client(host, port)
    clientObj.make_connection()

    if args.mode == 'w':
        clientObj.send_request()
    else:
        clientObj.recv_response()

except KeyboardInterrupt:
    logger.info('Client  closed')
    print('Client closed')



