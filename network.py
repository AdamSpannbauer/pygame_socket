import socket

FORMAT = "utf-8"
PORT = 5555


def get_host_name(default="127.0.0.1"):
    """Try to get host name and fall back to defaults"""
    try:
        return socket.gethostbyname(socket.gethostname())
    except socket.gaierror:
        try:
            return socket.gethostbyname(socket.gethostname() + ".local")
        except socket.gaierror:
            return default


class Network:
    def __init__(self, host=None, port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host is None:
            self.host = get_host_name()
        self.port = port
        self.pos = self.connect()

    @property
    def addr(self):
        return self.host, self.port

    def get_pos(self):
        return self.pos

    def connect(self):
        self.client.connect(self.addr)
        return self.client.recv(2048).decode(FORMAT)

    def send(self, data):
        try:
            self.client.send(data.encode(FORMAT))
            return self.client.recv(2048).decode(FORMAT)
        except BrokenPipeError:
            print("Broken pipe")


if __name__ == "__main__":
    n = Network(get_host_name(), 5555)
    print(n.send("test1"))
    print(n.send("test2"))
