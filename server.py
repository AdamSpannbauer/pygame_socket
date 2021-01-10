import socket
import threading
from network import get_host_name, PORT, FORMAT


# SERVER = get_host_name()
SERVER = "0.0.0.0"
print(f"[IP] using {SERVER}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

try:
    server.bind((SERVER, PORT))
except socket.error as e:
    print(str(e))


def read_pos(pos_str):
    x, y = pos_str.split(",")
    return int(x), int(y)


def encode_pos(xy):
    x, y = xy
    return f"{x},{y}".encode(FORMAT)


def handle_client(conn, addr, current_player, player_positions):
    print(f"[NEW CONNECTION] {addr} connected")

    player_position = player_positions[current_player]
    conn.send(encode_pos(player_position))

    connected = True
    while connected:
        try:
            player_position = conn.recv(8).decode(FORMAT)

            if not player_position:
                print(f"[DISCONNECTED] {addr} disconnected")
                break

            player_positions[current_player] = read_pos(player_position)
            other_player_position = player_positions[current_player == 0]

            print(f"[RECEIVED MESSAGE] {player_position}")
            print(f"[SENDING MESSAGE] {other_player_position}")
            conn.sendall(encode_pos(other_player_position))
        except:
            print(f"[DISCONNECTED] {addr} disconnected")
            break

    conn.close()


def start_server():
    server.listen(2)
    print(f"[LISTENING] server listening...")

    player_positions = [(0, 0), (100, 100)]
    current_player = 0
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, current_player, player_positions),
        )
        thread.start()

        active_connections = threading.activeCount() - 1
        current_player = 1

        print(f"[ACTIVE CONNECTIONS] {active_connections}")


print("[STARTING] server is starting...")
start_server()
