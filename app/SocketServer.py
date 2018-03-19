import socket
import re
import sys
from multiprocessing import Process, Queue, Manager, Pipe

UDP_PORT = 4047
READER = 0
WRITER = 1


class SocketServer:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.socketsend_queue = Queue()
        self.num_sequence = 1            # 0001 a 7FFF (hexadecimal)
        self.manager = Manager()
        self.addr_devices_list = self.manager.dict()
        self.pending_requests = self.manager.dict()
        self.lock = self.manager.Lock()
        self.receiver_process = Process(target=self.receiving)
        self.sender_process = Process(target=self.sending)

    def start_process(self):
        self.receiver_process.start()
        self.sender_process.start()

    def receiving(self):
        try:
            self.sock.bind(('', UDP_PORT))
        except OSError as e:
            print('Error {}'.format(e))
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                data = data.decode('ascii')
                print('[RECV] Recebido {}' .format(data))
                id = re.findall(r'ID=([A-F0-9]{4})', data)
                id_str = str(id[0])
                self.addr_devices_list[id_str] = addr
                self.answer_ack(data)
                if not self.keep_alive(data) and id_str in self.pending_requests:
                    answer_request = self.pending_requests[id_str]
                    answer_request['channels'][WRITER].send(data)
            except (OSError, KeyboardInterrupt, socket.error) as e:
                print('Error {}'.format(e))
                sys.exit(0)

    def sending(self):
        while True:
            try:
                device_id = self.socketsend_queue.get()
                # pending_requests:
                # {'device_id': {'data': '>QTT; bla blah<',
                #                'sent': True/False,
                #                'channels': (reader,writer)}}
                request = self.pending_requests[device_id]
                to_send = request['xvm']
                request.update(({'sent': True}))
                if bool(self.addr_devices_list.get(device_id)):
                    with self.lock:
                        self.sock.sendto((to_send + '\r\n').encode(), self.addr_devices_list[device_id])
                    print('[SEND] Enviado {} para {}'.format(to_send, self.addr_devices_list[device_id]))
                else:
                    print('[SEND] ID {} não possui um IP'.format(device_id))
            except (OSError, KeyboardInterrupt, socket.error) as e:
                print('Error {}'.format(e))
                sys.exit(0)

    @staticmethod
    def keep_alive(data):
        prefix = re.findall(r'\w[^,\r]+', data)
        if prefix[0] == 'RUS04':
            return True
        else:
            return False

    @staticmethod
    def multi_line_answer(data):
        # verifica se o comando é multiline (QISAL e QEPE)
        return True

    def answer_ack(self, data):
        default = '>ACK;ID={id};#{seq};*{crc}<'
        seq = re.findall(r'\w[^;\r]+', data)
        id = re.findall(r'ID=([A-F0-9]{4})', data)
        ack = default.format(id=id[0], seq=seq[2], crc=0)
        crc = hex(self.check_sum8_xor(ack))[2:].upper()
        ack = default.format(id=id[0], seq=seq[2], crc=str(crc))
        with self.lock:
            self.sock.sendto((ack + '\r\n').encode(), self.addr_devices_list[id[0]])

    @staticmethod
    def check_sum8_xor(data):
        crc = 0
        for ch in data:
            if ch == '*':
                break
            else:
                ch = ord(ch)
                crc = crc ^ ch
        return crc

    def send_command(self, device_id, cmd, mdt):
        if self.pending_requests.get(str(device_id)) is not None:
            return 'busy'
        if mdt == 'False':
            default = '>{cmd};ID={id};#{seq};*{crc}<'   # Virloc
        else:
            default = '>{cmd};ID={id}V;#{seq};*{crc}<'  # Vircom

        xvm_cmd = default.format(cmd=cmd.upper(),
                                 id=device_id,
                                 seq=str(hex(self.num_sequence))[2:].upper().zfill(4),
                                 crc=0)

        crc = hex(self.check_sum8_xor(xvm_cmd))[2:].upper().zfill(2)
        
        xvm_cmd = default.format(cmd=str(cmd).upper(),
                                 id=device_id,
                                 seq=str(hex(self.num_sequence))[2:].upper().zfill(4),
                                 crc=str(crc))

        new_request = {'channels': Pipe(), 'sent': False, 'xvm': xvm_cmd, 'cancelled': False}
        self.pending_requests[device_id] = new_request
        self.socketsend_queue.put(device_id)    # só avisa o processo SocketServer.sending()

        if self.num_sequence < 32767:
            self.num_sequence = self.num_sequence + 1
        else:
            self.num_sequence = 1
        return device_id

    def wait_response(self, request_id, timeout):
        request = self.pending_requests[request_id]
        reader = request['channels'][READER]
        # reader.poll = TRUE quando:
            # 1. chega algo em recvfrom que não é keep alive
            # 2. usuario cancelar o pedido
        if reader.poll(timeout):
            answer = reader.recv()
            del self.pending_requests[request_id]
            return answer
        else:
            del self.pending_requests[request_id]
            return 'timeout'

    def cancel_request(self, request_id):
        request = self.pending_requests[request_id]
        #request.update({'cancelled': True})
        request['channels'][WRITER].send('request cancelled')


