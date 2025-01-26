import socket
import psutil
import os
import time

SERVER_IP = "Your IP"  
PORT = 5000


def get_ram_info():
    mem = psutil.virtual_memory()
    return mem.available


def execute_task(task):
    print(f"[Cliente] Executando tarefa: {task}")
    os.system(task)


def main():
    print("[Cliente] Iniciando cliente...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        print(f"[Cliente] Conectado ao servidor {SERVER_IP}:{PORT}")

        try:
            buffer = ""  

            while True:

                data = s.recv(1024).decode()
                if not data:
                    break

                buffer += data  
                while "\n" in buffer: 
                    message, buffer = buffer.split("\n", 1)


                    if "RAM_Servidor" in message:
                        print(f"[Cliente] Status do servidor: {message.strip()}")

                    elif "PROCESSO:" in message:
                        task = message.split(":", 1)[1]
                        execute_task(task)

                ram_available = get_ram_info()
                ram_message = f"RAM_Cliente:{ram_available}\n"
                s.sendall(ram_message.encode())

                time.sleep(2)

        except Exception as e:
            print(f"[Cliente] Erro: {e}")
        finally:
            print("[Cliente] Encerrando conexão.")


if __name__ == "__main__":
    main()
