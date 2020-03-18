#!/usr/bin/env python3

import sys
import socket
import parsers
import generators

poc_host, poc_port = "192.168.2.100", 3001
poc_sequence_number = 4000

def answer_hello(conn, message):
    global poc_sequence_number
    poc_sequence_number += 1
    _message = parsers.parse_hello_message(message)
    ack_bytes = generators.generate_ack_message(_message, poc_sequence_number)
    print("----------------------------")
    print("[ACK] => DCA")
    print("----------------------------")
    parsers.prettyprint(ack_bytes)
    conn.send(ack_bytes)

if __name__ == "__main__":
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((poc_host, poc_port))
        sock.listen()
        conn, addr = sock.accept()
        with conn:
            print("Connected by {}".format(addr))
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                data_str = data.strip().decode("utf-8")
                if "HEL.R01" in data_str:
                    print("----------------------------")
                    print("DCA => [HELLO]")
                    print("----------------------------")
                    parsers.prettyprint(data)

                    answer_hello(conn, data_str)

                elif "ESC.R01" in data_str and "OTH" in data_str:
                    raise Exception("!!!BAD ACK!!!")
                else:
                    print("----------------------------")
                    print("DCA => [???]")
                    print("----------------------------")
                    parsers.prettyprint(data)

    except Exception as e:
        print("ERROR: {}".format(e))
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        sock.close()
