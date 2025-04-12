import socket

HOST = ''  # Bind to all interfaces
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on port {PORT}...")

    while True:
        conn, addr = s.accept()
        with conn:
            # print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    # print(f"Connection with {addr} closed.")
                    break
                print("Received:", data.decode())
