import socket
import re
import sys
import json
from multiprocessing import Process, Queue, Manager, Pipe

UDP_PORT = 4047
READER = 0
WRITER = 1

# usar @staticmethod ou @classmethod ?
# com class não usaria __init__, declararia td como global

class SocketServer:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.request_queue = Queue()     # fila para receber os comandos dos clientes (testar o recebimento de tupla)
        self.socketsend_queue = Queue()  # fila de envio (sempre com uma tupla)
        self.socketrecv_queue = Queue()  # fila de recebimento (qualquer coisa)
        self.num_sequence = 1            # sequencia das mensagens 0001 a 7FFF (hexadecimal)
        self.manager = Manager()
        self.addr_devices_list = self.manager.dict()
        self.pending_requests = self.manager.dict()

    def init_queues(self):
        self.receiver_process = Process(target=self.receiving)
        self.sender_process = Process(target=self.sending)                                  
        self.receiver_process.start()
        self.sender_process.start()

    def receiving(self):
        self.sock.bind(('', UDP_PORT))
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode('ascii')
                #print('\n\n')
                print('[RECV] Recebido {} de {}' .format(data, addr))
                id = re.findall(r'ID=([A-F0-9]{4})', data)
                id_str = str(id[0])
                # send_ack (sendto)
                self.addr_devices_list[id_str] = addr
                self.answer_ack(data)
                if not self.iskeepalive(data):
                    # self.pending_request['4116']['channels'][1] é o pipe_writer
                    # quem chama await_response() lá embaixo chama o pipe_reader.recv()
                    # correspondente, então ele vai receber este 'data' aqui:
                    print('RECV pending_requests.send(data) {}' .format(self.pending_requests[id_str]))
                    self.pending_requests[id_str]['channels'][WRITER].send(data)

                    #self.socketrecv_queue.put(data)
            except(EOFError, KeyboardInterrupt):
                print('Exit receiving ...')
                sys.exit(0)

    def sending(self):
        while True:
            try:
                # só um aviso de que tem coisa nova no self.pending_requests
                _work = self.socketsend_queue.get()
                #_work.get para pegar o ID que teve uma nova requisição

                # aqui vai ter que olhar dentro de self.pending_requests e
                # determinar quais itens devem ser enviados agora
                # Lembrando: a estrutura do pending_requests é
                # {'device_id': {'data': '>QTT; bla blah<',
                #                'sent': True/False,
                #                'channels': (reader,writer)}}

                # TO DO: olhar dentro do self.pending_requests e ver qual comandos enviar.
                # ROG: _work está com o device_id que precisa ser processado (quando enviar/não enviar?)
                #print('pending_requests: {}' .format(self.pending_requests))
                #print('_work: {}' .format(_work))
                #print('to_send: {}' .format(self.pending_requests[_work]['xvm']))
                #print('addr_devices_list {}' .format(self.addr_devices_list))
                to_send = self.pending_requests[_work]['xvm']
                self.pending_requests[_work]['sent'] = True
                device_id = _work

                # esse bloco não funciona agora pq device_id e to_send ainda não foram
                # lidos de dentro do self.pending_requests                
                if bool(self.addr_devices_list.get(device_id)):
                    self.sock.sendto((to_send + '\r\n').encode(), self.addr_devices_list[device_id])
                    # essa linha localhost usa apenas quando for testar sem virloc
                    # sock.sendto((msg[0] + '\r\n').encode(), ('localhost', 4095))
                    print('[SEND] Enviado {} para {}'.format(to_send, self.addr_devices_list[device_id]))
                else:
                    print('[SEND] ID {} não possui um IP'.format(device_id))
            except(EOFError, KeyboardInterrupt):
                print('Exit sending ...')
                sys.exit(0)

    @staticmethod
    def iskeepalive(data):
        prefix = re.findall(r'\w[^,\r]+', data)
        if prefix[0] == 'RUS04':
            return True
        else:
            return False

    def answer_ack(self, data):
        default = '>ACK;ID={id};#{seq};*{crc}<'
        seq = re.findall(r'\w[^;\r]+', data)
        id = re.findall(r'ID=([A-F0-9]{4})', data)
        ack = default.format(id=id[0], seq=seq[2], crc=0)
        crc = hex(self.calcula_crc(ack))[2:].upper()
        ack = default.format(id=id[0], seq=seq[2], crc=str(crc))
        tuple_ack = (ack, id[0])
        self.sock.sendto((ack + '\r\n').encode(), self.addr_devices_list[id[0]])
        print('[SEND] Enviado {} para {}'.format(ack, self.addr_devices_list[id[0]]))
        #new_request = {'channels': Pipe(), 'sent': False, 'xvm': ack}
        #self.pending_requests[id[0]] = new_request
        #self.socketsend_queue.put(id[0])

    @staticmethod
    def calcula_crc(data):
        crc = 0
        for ch in data:
            if ch == '*':
                break
            else:
                ch = ord(ch)
                crc = crc ^ ch
        return crc

    def send_command(self, device_id, cmd):
        print('SELF.PENDING REQUESTS {}' .format(self.pending_requests))
        if device_id in self.pending_requests is False:
            return 'busy'
        #if self.pending_requests(device_id) is not None:
        #    return 'busy'
        # se pending_requets, pro id solicitado, já tem algo -> BUSY
        default = '>{cmd};ID={id};#{seq};*{crc}<'

        xvm_cmd = default.format(cmd=cmd.upper(),
                                 id=device_id,
                                 seq=str(hex(self.num_sequence))[2:].upper().zfill(4),
                                 crc=0)

        crc = hex(self.calcula_crc(xvm_cmd))[2:].upper().zfill(2)
        
        xvm_cmd = default.format(cmd=str(cmd).upper(),
                                 id=device_id,
                                 seq=str(hex(self.num_sequence))[2:].upper().zfill(4),
                                 crc=str(crc))

        new_request = {'channels': Pipe(), 'sent': False, 'xvm': xvm_cmd}
        self.pending_requests[device_id] = new_request
        # pending_requests é dict, recebeu um new_request no id 4116

        self.socketsend_queue.put(device_id) # só avisa o processo SocketServer.sending()
        # coloca na fila do sock_send o id que precisa ser enviado

        if self.num_sequence < 32767:
            self.num_sequence = self.num_sequence + 1
        else:
            self.num_sequence = 1
        return device_id

    def wait_response(self, request_id, timeout=5):
        request = self.pending_requests[request_id]
        #reader = request[request_id]['channels'][READER] # não precisa do request_id
        reader = request['channels'][READER]

        if reader.poll(timeout):
            return reader.recv()
        else:
            return 'timeout'
