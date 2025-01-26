import socket
import psutil
import threading
import time
import os

HOST = "IP Server"
PORT = 5000

clients = []


def get_ram_info():
    mem = psutil.virtual_memory()
    return mem.available, mem.total


def handle_client(conn, addr):
    print(f"[Servidor] Conexão estabelecida com {addr}")
    clients.append(conn)
    try:
        while True:
            local_ram, total_ram = get_ram_info()
            conn.sendall(f"RAM_Servidor:{local_ram}/{total_ram}\n".encode())

            data = conn.recv(1024).decode().strip()
            if not data:
                break

            print(f"[Servidor] Status do cliente {addr}: {data}")

            client_ram = int(data.split(":")[1])
            if local_ram > client_ram:
                task = "PROCESSO:echo Executando no servidor...\n"
                print("[Servidor] Executando localmente...")
                execute_task(task.split(":")[1])
            else:
                task = "PROCESSO:echo Executando no cliente...\n"
                print(f"[Servidor] Enviando tarefa para o cliente {addr}")
                conn.sendall(task.encode())

            time.sleep(2)

    except Exception as e:
        print(f"[Servidor] Erro com {addr}: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"[Servidor] Conexão encerrada com {addr}")


def execute_task(task):
    """Executa um comando localmente."""
    os.system(task)


def main():
    print("[Servidor] Iniciando servidor...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servidor] Aguardando conexões na porta {PORT}...")

        while True:
            try:
                conn, addr = s.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.start()
                print(f"[Servidor] Clientes conectados: {threading.active_count() - 1}")
            except KeyboardInterrupt:
                print("\n[Servidor] Encerrando servidor...")
                break


if __name__ == "__main__":
    main()
