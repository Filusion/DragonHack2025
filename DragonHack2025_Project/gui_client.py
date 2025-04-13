import socket
import threading
import tkinter as tk
from tkinter import font as tkfont

def listen_for_alert():
    while True:
        try:
            data = sock.recv(1024)
            if data.decode().strip() == "FALL_ALERT":
                show_alert_ui()
        except Exception as e:
            print(f"❌ Error: {e}")
            break

def show_alert_ui():
    alert_label.pack_forget()

    alert_frame = tk.Frame(root, bg="white")
    alert_frame.pack(expand=True, fill="both")

    # Placeholder for icon (you can load an actual image here)
    icon = tk.Label(
        alert_frame,
        text="💙➕",  # Simulated heart + cross
        font=("Helvetica", 60),
        bg="white"
    )
    icon.pack(pady=(30, 10))

    # HealthAlert title
    title = tk.Label(
        alert_frame,
        text="HealthAlert",
        font=("Helvetica Neue", 22, "bold"),
        fg="#234EA4",
        bg="white"
    )
    title.pack()

    # Alert message
    alert_msg = tk.Label(
        alert_frame,
        text="Your elderly person has\nfallen",
        font=("Helvetica Neue", 18, "bold"),
        fg="#1E1E1E",
        bg="white",
        pady=10
    )
    alert_msg.pack()

    # Subtext
    subtext = tk.Label(
        alert_frame,
        text="Login to Stay healthy and fit",
        font=("Helvetica Neue", 12),
        fg="#888888",
        bg="white"
    )
    subtext.pack(pady=(0, 20))

    # Call emergency services button
    call_btn = tk.Button(
        alert_frame,
        text="Call emergency services",
        font=("Helvetica Neue", 14, "bold"),
        bg="#3D73DD",
        fg="white",
        activebackground="#2f5db8",
        relief="flat",
        padx=20,
        pady=10,
        borderwidth=0
    )
    call_btn.pack(pady=(0, 10), ipadx=10, ipady=2)

    # "I am going to check" button
    check_btn = tk.Button(
        alert_frame,
        text="I am going to check",
        font=("Helvetica Neue", 14),
        bg="white",
        fg="#3D73DD",
        highlightbackground="#3D73DD",
        highlightcolor="#3D73DD",
        highlightthickness=2,
        borderwidth=0,
        padx=20,
        pady=10
    )
    check_btn.pack(pady=(0, 20), ipadx=10, ipady=2)

# GUI Setup
root = tk.Tk()
root.title("Fall Detection Alert")
root.geometry("400x600")
root.configure(bg="white")

alert_label = tk.Label(
    root,
    text="Waiting for alert...",
    font=("Helvetica", 18, "bold"),
    fg="#333",
    bg="white",
    wraplength=380,
    justify="center",
    padx=20,
    pady=40
)
alert_label.pack(expand=True)

# Connect to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 10000))

# Start listening
threading.Thread(target=listen_for_alert, daemon=True).start()

root.mainloop()