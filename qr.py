# WiFi QR Code Generator using qrcode library

import qrcode

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

def main():
    # User inputs
    ssid = input("Enter WiFi SSID: ").strip()
    password = ''
    encryption = input("Enter Encryption Type (WPA, WEP, nopass): ").strip().upper()

    if not ssid:
        print("SSID is required.")
        return

    if encryption not in ['WPA', 'WEP', 'NOPASS']:
        print("Invalid encryption type. Choose from WPA, WEP, or nopass.")
        return

    if encryption != 'NOPASS':
        password = input("Enter WiFi Password: ").strip()

    # Generate WiFi configuration string
    wifi_string = generate_wifi_string(ssid, password, encryption)
    print("\nWiFi Configuration String:")
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
    img.save('wifi_qr_code.png')
    print("\nQR code generated and saved as 'wifi_qr_code.png'.")

if __name__ == '__main__':
    main()
