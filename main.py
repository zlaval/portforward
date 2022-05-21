import logging
import os
import socket
import threading

format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)

def transfer(src, dst):
    src_address, src_port = src.getsockname()
    dst_address, dst_port = dst.getsockname()
    while True:
        try:
            buffer = src.recv(4096)
            dst.send(buffer)
        except Exception as e:
            logging.error(repr(e))
            break
    logging.warning(f"Closing connect {src_address, src_port}! ")
    src.close()
    logging.warning(f"Closing connect {dst_address, dst_port}! ")
    dst.close()


def server(local_host, local_port, remote_host, remote_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((local_host, local_port))
    server_socket.listen(0x40)
    logging.info(f"Server started {local_host, local_port}")
    logging.info(f"Connect to {local_host, local_port} to get the content of {remote_host, remote_port}")
    while True:
        src_socket, src_address = server_socket.accept()
        logging.info(f"[Establishing] {src_address} -> {local_host, local_port} -> ? -> {remote_host, remote_port}")
        try:
            dst_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            dst_socket.connect((remote_host, remote_port))
            logging.info(
                f"[OK] {src_address} -> {local_host, local_port} -> {dst_socket.getsockname()} -> {remote_host, remote_port}")
            s = threading.Thread(target=transfer, args=(dst_socket, src_socket))
            r = threading.Thread(target=transfer, args=(src_socket, dst_socket))
            s.start()
            r.start()
        except Exception as e:
            logging.error(repr(e))


def main():
    LISTEN_PORT = 5000
    LISTEN_HOST = 'localhost'
    CONNECT_HOST = os.environ.get('CONNECT_HOST')
    CONNECT_PORT = int(os.environ.get('CONNECT_PORT'))

    logging.info(f"App starts, connect to  {CONNECT_HOST, CONNECT_PORT}")

    server(LISTEN_HOST, LISTEN_PORT,
           CONNECT_HOST, CONNECT_PORT)


if __name__ == "__main__":
    main()
