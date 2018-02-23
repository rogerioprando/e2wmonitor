from multiprocessing import Process, Pipe, Manager
import time

manager = Manager()
pipes = manager.dict()


class Server:
    def __init__(self, manager):
        self.manager = manager
        self.pipes = self.manager.dict()
        
    def start(self):
        self.runner = Process(target=self.run)
        self.runner.start()
        
    def run(self):
        print('waiting to run')
        time.sleep(2)
        print('running')
        for k,p in self.pipes.items():
            print('for items')
            p[1][1].send('response for %s is %s' % (p[0],'Heey'))

    def send_request(self, request_id, request_data):
        self.pipes[request_id] = (request_data, Pipe())

    def await_response(self, request_id):
        reader = self.pipes[request_id][1][0]
        if reader.poll(5):
            return reader.recv()

if __name__ == '__main__':
    manager = Manager()
    proc = Server(manager)      # obj process
    proc.start()                # start process -> target run()

    my_id = 'hey'
    proc.send_request(my_id, 'a request')   # request with id and a command
    print('made send_request, now waiting')
    response = proc.await_response(my_id)   # wait the answer from sent id
    print('done')
    print(response)
