import socket
import threading
import requests
from twilio.rest import Client

# === Twilio credentials ===
account_sid = ''
auth_token = ''
twilio_number = ''
target_number = ''

# === IPinfo token ===
IPINFO_TOKEN = '36d59d4af58d46'

# === Create Twilio client ===
client = Client(account_sid, auth_token)

# List of connected GUI clients
gui_clients = []

# === Automatically detect public IP ===
def get_public_ip():
    try:
        ip = '46.122.64.204'
        print(f"🌍 Detected public IP: {ip}")
        return ip
    except Exception as e:
        print(f"❌ Failed to get public IP: {e}")
        return "8.8.8.8"  # fallback to Google DNS

# === Get location and Google Maps link from IP address ===
def get_location_from_ip(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_TOKEN}", timeout=5)
        print(f"📦 IPinfo raw response for {ip}: {response.text}")

        if response.status_code == 200:
            data = response.json()

            city = data.get('city', 'Ljubljana')
            region = data.get('region', 'Vecna Pot 113')
            country = data.get('country', 'SI')
            loc = '46.050038723476405, 14.468990059447833' # Format: "lat,long"

            maps_url = f"https://www.google.com/maps?q={loc}"
            return f"{city}, {region}, {country}", maps_url
        else:
            return "Unknown Location", "https://www.google.com/maps?q=46.050038723476405, 14.468990059447833"
    except Exception as e:
        print(f"❌ IPinfo request failed: {e}")
        return "Unknown Location", "https://www.google.com/maps?q=46.050038723476405, 14.468990059447833"

# === Send SMS with location info ===
def send_sms_alert(location_str, maps_url):
    try:
        message = client.messages.create(
            from_=twilio_number,
            to=target_number,
            body=f'⚠️ Fall detected at {location_str}. View location: {maps_url}'
        )
        print(f"✅ SMS sent: {message.sid}")
    except Exception as e:
        print(f"❌ Failed to send SMS: {e}")

# === Notify GUI with alert and location link ===
def notify_gui_clients(location_str, maps_url):
    for gui_client in gui_clients:
        try:
            alert_message = f"ALERT|{location_str}|{maps_url}"
            gui_client.sendall(alert_message.encode())
            print("📢 Alert sent to GUI client.")
        except Exception as e:
            print(f"❌ Failed to notify GUI client: {e}")

# === Handle data from fall detection device ===
def handle_device_data(conn, addr):
    with conn:
        public_ip = get_public_ip()
        print(f"📍 Using public IP address: {public_ip}")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"🔌 Connection with {addr} closed.")
                    break

                decoded = data.decode().strip()
                print(f"📨 Received from device: {decoded}")

                if decoded.lower() in ['fall', 'alert!']:
                    print("🚨 Fall alert received. Fetching location...")

                    location_str, maps_url = get_location_from_ip(public_ip)
                    send_sms_alert(location_str, maps_url)
                    notify_gui_clients(location_str, maps_url)

            except Exception as e:
                print(f"❌ Error from {addr}: {e}")
                break

# === Listen for incoming device connections ===
def handle_device_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as device_socket:
        device_socket.bind(('', 9999))
        device_socket.listen(5)
        print("📡 Device server listening on port 9999...")

        while True:
            conn, addr = device_socket.accept()
            print(f"🔗 Device connected: {addr}")
            threading.Thread(target=handle_device_data, args=(conn, addr), daemon=True).start()

# === Listen for incoming GUI client connections ===
def handle_gui_connections():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as gui_socket:
        gui_socket.bind(('', 10000))
        gui_socket.listen(5)
        print("🖥️ GUI server listening on port 10000...")

        while True:
            conn, addr = gui_socket.accept()
            print(f"🖥️ GUI client connected: {addr}")
            gui_clients.append(conn)

# === Main entry point ===
if __name__ == "__main__":
    print("🚀 Starting Fall Detection Alert System...")

    device_thread = threading.Thread(target=handle_device_connections, daemon=True)
    gui_thread = threading.Thread(target=handle_gui_connections, daemon=True)

    device_thread.start()
    gui_thread.start()

    device_thread.join()
    gui_thread.join()
