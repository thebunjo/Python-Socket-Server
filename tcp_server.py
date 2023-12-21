import socket
import sys
import time
import psutil
from colorama import Style, init, Fore
import multiprocessing
import threading
import logging
import platform

init()

logging.basicConfig(filename='server_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Server:
    SERVER_IP, SERVER_PORT = '192.168.1.94', 4545
    SERVER_ADDR, MAX_CONNS = (SERVER_IP, SERVER_PORT), 10
    BUFFER_SIZE = 2048

    server_socket = None

    class ClientManager:
        def __init__(self):
            self.client_connections = []

        def add_client(self, connection, address):
            self.client_connections.append((connection, address))

            logging.info("Connected to {}. Total clients: {}"
                         .format(address, len(self.client_connections)))

        def remove_client(self, connection):
            connection, address = connection
            self.client_connections.remove((connection, address))
            logging.info("Closed connection to {}. Total clients: {}"
                         .format(address, len(self.client_connections)))

    class Additionals:
        class Time:
            @staticmethod
            def get_time_now():
                current_time = time.localtime()
                formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                formatted_date = time.strftime("%Y-%m-%d", current_time)
                formatted_day = time.strftime("%A", current_time)

                print("Date: {}{}{}".format(Fore.LIGHTBLUE_EX, formatted_date, Style.RESET_ALL))
                print("Day: {}{}{}".format(Fore.LIGHTBLUE_EX, formatted_day, Style.RESET_ALL))
                print("Time: {}{}{}\n".format(Fore.LIGHTBLUE_EX, formatted_time, Style.RESET_ALL))

                logging.info("Current date: {}".format(formatted_date))
                logging.info("Current day: {}".format(formatted_day))
                logging.info("Current time: {}".format(formatted_time))

        class CPU:
            @staticmethod
            def get_cpu_info():
                print("Processors: \n")

                cpu_info = platform.processor()
                print("Processor: {}{}{}"
                      .format(Fore.LIGHTWHITE_EX, cpu_info, Style.RESET_ALL))

                cpu_count = multiprocessing.cpu_count()
                print("Processor Cores: {}{}{}\n"
                      .format(Fore.LIGHTWHITE_EX, cpu_count, Style.RESET_ALL))

                logging.info("Processor: {}".format(cpu_info))
                logging.info("Processor Cores: {}".format(cpu_count))

        class RAM:
            @staticmethod
            def get_ram_usage():
                ram = psutil.virtual_memory()

                total_ram = ram.total / (1024 ** 3)
                used_ram = ram.used / (1024 ** 3)
                free_ram = ram.available / (1024 ** 3)
                ram_percent = ram.percent

                print("\nRAM State: \n\t")
                print("Total RAM: {}{:.2f} GB{}".format(
                    Fore.MAGENTA, total_ram, Style.RESET_ALL))
                print("Used RAM: {}{:.2f} GB{}".format(
                    Fore.MAGENTA, used_ram, Style.RESET_ALL))
                print("Free RAM: {}{:.2f} GB{}".format(
                    Fore.MAGENTA, free_ram, Style.RESET_ALL))
                print("RAM Percent: {}{:.2f}%\n{}".format(
                    Fore.MAGENTA, ram_percent, Style.RESET_ALL))

                logging.info("Total RAM: {:.2f} GB".format(total_ram))
                logging.info("Used RAM: {:.2f} GB".format(used_ram))
                logging.info("Free RAM: {:.2f} GB".format(free_ram))
                logging.info("RAM Percent: {:.2f}%".format(ram_percent))

        class Credentials:
            @staticmethod
            def server_credentials():
                print("Server: ")

                print("\nSERVER_IP: {}{}{}".format(
                    Fore.LIGHTWHITE_EX,
                    Server.SERVER_IP,
                    Style.RESET_ALL))

                print("SERVER_PORT: {}{}{}".format(
                    Fore.LIGHTWHITE_EX,
                    Server.SERVER_PORT,
                    Style.RESET_ALL))

                logging.info("Server IP: {}".format(Server.SERVER_IP))
                logging.info("Server Port: {}".format(Server.SERVER_PORT))

    @staticmethod
    def handle_server():
        try:
            Server.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            Server.server_socket.bind(Server.SERVER_ADDR)

            logging.info("Server socket created and bound to {}".format(Server.SERVER_ADDR))

        except socket.gaierror as socket_gai_error:
            print("Error: {}{}{}".format(Fore.RED, socket_gai_error, Style.RESET_ALL))
            logging.error("Socket gaierror: {}".format(socket_gai_error))

        except OSError as os_error:
            print("Error: {}{}{}".format(Fore.RED, os_error, Style.RESET_ALL))
            logging.error("OSError: {}".format(os_error))

    @staticmethod
    def receive_data(client_connection, client_addr):
        try:
            client_message = client_connection.recv(Server.BUFFER_SIZE)
            print("Received DATA from: {}{}\nData: {}"
                  .format(client_addr[0], client_addr[1], client_message.decode('utf-8')))

        except Exception as e:
            print("Error while receiving data: {}".format(e))
            logging.error("Error while receiving data: {}".format(e))

    @staticmethod
    def start_listen():
        try:
            client_manager = Server.ClientManager()

            Server.server_socket.listen(Server.MAX_CONNS)
            print("{}Server is listening to connections on {}:{} {}\n"
                         .format(Fore.YELLOW, Server.SERVER_IP, Server.SERVER_PORT, Style.RESET_ALL))

            logging.info("Server is listening to connections on {}:{}"
                         .format(Server.SERVER_IP, Server.SERVER_PORT))

            while True:
                client_connection, client_addr = Server.server_socket.accept()
                client_manager.add_client(client_connection, client_addr)

                receive_thread = threading.Thread(
                    target=Server.receive_data,
                    args=(client_connection, client_addr)).start()

        except socket.error as socket_error:
            print("Error: {}{}{}"
                  .format(Fore.RED, socket_error, Style.RESET_ALL))
            logging.error("Socket error: {}".format(socket_error))

        except KeyboardInterrupt as keyboard_interrupt:
            print("Server closed: {}{}{}"
                  .format(Fore.YELLOW, keyboard_interrupt, Style.RESET_ALL))
            logging.info("Server closed due to keyboard interrupt")
            sys.exit(0)

    @staticmethod
    def main():
        Server.handle_server()

        Server.Additionals.Time.get_time_now()
        Server.Additionals.Credentials.server_credentials()
        Server.Additionals.RAM.get_ram_usage()
        Server.Additionals.CPU.get_cpu_info()

        Server.start_listen()


if __name__ == "__main__":
    Server.main()
