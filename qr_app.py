# WiFi QR Code Generator Desktop App using Tkinter and qrcode library

import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import qrcode
import io

def escape_string(s):
    # Escapes special characters in SSID and password
    return s.replace('\\', '\\\\').replace(';', '\\;').replace(',', '\\,').replace(':', '\\:').replace('"', '\\"')

def generate_wifi_string(ssid, password, encryption):
    # Constructs the WiFi configuration string
    wifi_string = f"WIFI:T:{encryption};S:{escape_string(ssid)};"
    if encryption != 'nopass':
        wifi_string += f"P:{escape_string(password)};"
    wifi_string += ";"
    return wifi_string

def generate_qr_code():
    ssid = ssid_entry.get().strip()
    password = password_entry.get().strip()
    encryption = encryption_var.get()

    if not ssid:
        messagebox.showerror("Error", "SSID is required.")
        return

    if encryption not in ['WPA', 'WEP', 'nopass']:
        messagebox.showerror("Error", "Invalid encryption type.")
        return

    if encryption != 'nopass' and not password:
        messagebox.showerror("Error", "Password is required for WPA/WEP encryption.")
        return

    # Generate WiFi configuration string
    wifi_string = generate_wifi_string(ssid, password, encryption)
    print("WiFi Configuration String:")
    print(wifi_string)

    # Generate QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_string)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # Display QR code in GUI
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    qr_image = Image.open(img_buffer)
    qr_photo = ImageTk.PhotoImage(qr_image)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo  # Keep a reference
    save_button.config(state=tk.NORMAL)

def save_qr_code():
    ssid = ssid_entry.get().strip()
    if not ssid:
        ssid = "wifi_qr_code"
    else:
        ssid = ssid.replace(" ", "_")

    file_name = f"{ssid}.png"
    img_buffer = io.BytesIO()
    qr_label.image._PhotoImage__photo.write(img_buffer, format='PNG')
    with open(file_name, 'wb') as f:
        f.write(img_buffer.getvalue())
    messagebox.showinfo("Saved", f"QR code saved as '{file_name}'.")

# Set up the main application window
app = tk.Tk()
app.title("WiFi QR Code Generator")
app.resizable(False, False)

# SSID input
ssid_label = tk.Label(app, text="WiFi Network Name (SSID):")
ssid_label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
ssid_entry = tk.Entry(app, width=30)
ssid_entry.grid(row=0, column=1, padx=5, pady=5)

# Password input
password_label = tk.Label(app, text="Password:")
password_label.grid(row=1, column=0, sticky='e', padx=5, pady=5)
password_entry = tk.Entry(app, width=30, show='*')
password_entry.grid(row=1, column=1, padx=5, pady=5)

# Encryption type
encryption_label = tk.Label(app, text="Encryption Type:")
encryption_label.grid(row=2, column=0, sticky='e', padx=5, pady=5)
encryption_var = tk.StringVar(value='WPA')
encryption_menu = tk.OptionMenu(app, encryption_var, 'WPA', 'WEP', 'nopass')
encryption_menu.grid(row=2, column=1, padx=5, pady=5, sticky='w')

# Generate button
generate_button = tk.Button(app, text="Generate QR Code", command=generate_qr_code)
generate_button.grid(row=3, column=0, columnspan=2, pady=10)

# QR code display
qr_label = tk.Label(app)
qr_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

# Save button
save_button = tk.Button(app, text="Save QR Code", command=save_qr_code, state=tk.DISABLED)
save_button.grid(row=5, column=0, columnspan=2, pady=10)

app.mainloop()
