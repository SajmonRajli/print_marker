import socket



# задаем IP-адрес и порт сервера
host = 'localhost'
port = 23

class Printer():
    def __init__(self):
        # создаем объект сокета
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # подключаемся к серверу
        self.client_socket.connect((host, port))


    # отправка запроса
    def request(self, request):
        self.client_socket.send(request.encode())

    # печать
    def print(self, DATA):
        request = f'<SOH>PRINT[<STX>{DATA}<ETX>]<EOT>'
        self.client_socket.send(request.encode())
        # ждем ответа от принтера
        r = self.client_socket.recv(1024)
        return r.decode() 
    
    # остановка печати
    def stop_print(self):
        request = '<SOH>STOP<EOT>'
        self.client_socket.send(request.encode())

    # получение статуса
    def status_print(self):
        request = '<SOH>STATUS<EOT>'
        self.client_socket.send(request.encode())
        r = self.client_socket.recv(1024)
        return r.decode() 

    # отжидание ответа
    def responce(self):
        r = self.client_socket.recv(1024)
        return r.decode() 

if __name__ == '__main__':
    TCP = Printer()
    request = '<SOH>CMD[<STX>DATA<ETX>]<EOT>'
    print(TCP.request(request))
    
