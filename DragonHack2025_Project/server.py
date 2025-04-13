import socket
import threading
from twilio.rest import Client

# Twilio credentials (replace with your actual credentials)
account_sid = 'AC2791c0de67b7cc7cdb85e67e5dfe6c70'
auth_token = 'c9e57380f3da029f91ad3dac013c3988'
twilio_number = '+13419004057'
target_number = '+38669738651'

# Create Twilio client
client = Client(account_sid, auth_token)

# GUI client connections
gui_clients = []

def send_sms_alert():
    try:
        message = client.messages.create(
            from_=twilio_number,
            to=target_number,
            body='⚠️ Alert: A fall has been detected. Please check immediately.'
        )
        print(f"✅ SMS sent successfully: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")

def notify_gui_clients():
    for gui_client in gui_clients:
        try:
            gui_client.sendall(b"FALL_ALERT")
            print("📢 Alert sent to GUI client.")
        except Exception as e:
            print(f"❌ Failed to notify GUI client: {e}")

def handle_device_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as device_socket:
        device_socket.bind(('', 9999))
        device_socket.listen(5)
        print("📡 Device server listening on port 9999...")

        while True:
            conn, addr = device_socket.accept()
            print(f"🔗 Device connected: {addr}")
            threading.Thread(target=handle_device_data, args=(conn, addr), daemon=True).start()

def handle_device_data(conn, addr):
    with conn:
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"🔌 Connection with {addr} closed.")
                    break

                decoded = data.decode().strip()
                print(f"📨 Received from device: {decoded}")

                if decoded.lower() in ['fall', 'alert!']:
                    print("🚨 Fall alert received. Sending SMS and notifying GUI...")
                    send_sms_alert()
                    notify_gui_clients()

            except Exception as e:
                print(f"❌ Error from {addr}: {e}")
                break

def handle_gui_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gui_socket:
        gui_socket.bind(('', 10000))
        gui_socket.listen(5)
        print("🖥️ GUI server listening on port 10000...")

        while True:
            conn, addr = gui_socket.accept()
            print(f"🖥️ GUI client connected: {addr}")
            gui_clients.append(conn)

# Start servers
threading.Thread(target=handle_device_connections, daemon=True).start()
threading.Thread(target=handle_gui_connections, daemon=True).start()

input("🚀 Server is running. Press Enter to stop...\n")
