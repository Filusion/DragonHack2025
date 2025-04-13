import socket
import threading
import tkinter as tk
import webbrowser

alert_triggered = False


def listen_for_alert():
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break

            decoded = data.decode().strip()
            print(f"📨 Received: {decoded}")

            if decoded.startswith("ALERT|"):
                parts = decoded.split('|')
                if len(parts) >= 3:
                    location = parts[1]
                    maps_url = parts[2]

                    # Update UI in main thread
                    root.after(0, lambda l=location, m=maps_url: show_alert_ui(l, m))

        except Exception as e:
            print(f"❌ Error receiving alert: {e}")
            break


def open_map_link(url):
    def handler(event=None):
        print(f"🌐 Opening URL: {url}")
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            print(f"❌ Failed to open link: {e}")

    return handler


def show_alert_ui(location_str, maps_url):
    global alert_triggered
    if alert_triggered:
        return
    alert_triggered = True

    alert_label.pack_forget()

    alert_frame = tk.Frame(root, bg="white")
    alert_frame.pack(expand=True, fill="both")

    # Icon
    icon = tk.Label(alert_frame, text="💙➕", font=("Helvetica", 60), bg="white")
    icon.pack(pady=(30, 10))

    # Title
    title = tk.Label(alert_frame, text="HealthAlert", font=("Helvetica Neue", 22, "bold"),
                     fg="#234EA4", bg="white")
    title.pack()

    # Alert message
    alert_msg = tk.Label(alert_frame, text="Your elderly person has\nfallen",
                         font=("Helvetica Neue", 18, "bold"), fg="#1E1E1E", bg="white", pady=10)
    alert_msg.pack()

    # Location display
    location_display = tk.Label(alert_frame, text=location_str,
                                font=("Helvetica Neue", 14), fg="#555555", bg="white")
    location_display.pack(pady=(0, 20))

    # Call button
    call_btn = tk.Button(alert_frame, text="Call emergency services",
                         font=("Helvetica Neue", 14, "bold"), bg="#3D73DD", fg="white",
                         activebackground="#2f5db8", relief="flat", padx=20, pady=10, borderwidth=0)
    call_btn.pack(pady=(0, 10), ipadx=10, ipady=2)

    # Check button
    check_btn = tk.Button(alert_frame, text="I am going to check",
                          font=("Helvetica Neue", 14), bg="white", fg="#3D73DD",
                          highlightbackground="#3D73DD", highlightcolor="#3D73DD",
                          highlightthickness=2, borderwidth=0, padx=20, pady=10)
    check_btn.pack(pady=(0, 20), ipadx=10, ipady=2)

    # Map link
    location_label = tk.Label(alert_frame, text="📍 View location on map",
                              font=("Helvetica Neue", 12, "underline"), fg="#3D73DD", bg="white",
                              cursor="hand2")
    location_label.pack(pady=(10, 10))
    location_label.bind("<Button-1>", open_map_link(maps_url))


# GUI Setup
root = tk.Tk()
root.title("Fall Detection Alert")
root.geometry("400x600")
root.configure(bg="white")

alert_label = tk.Label(root, text="Everything seems to be fine right now",
                       font=("Helvetica", 18, "bold"), fg="#333", bg="white",
                       wraplength=380, justify="center", padx=20, pady=40)
alert_label.pack(expand=True)

# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 10000))  # Change to server IP if needed

# Start listening thread
threading.Thread(target=listen_for_alert, daemon=True).start()

# Start GUI
root.mainloop()