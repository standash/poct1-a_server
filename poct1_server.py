#!/usr/bin/env python3

import sys
import socket
import parsers
import generators
import traceback

poc_host, poc_port = "192.168.2.100", 3001
poc_sequence_number = 4000


def answer_hello(conn, message):
    global poc_sequence_number
    poc_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parsers.parse_incoming_message(fields, message)
    ack_bytes = generators.generate_ack_message(fields, poc_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(ack_bytes)
    #
    conn.send(ack_bytes)
    return fields


def answer_device_status(conn, message):
    global poc_sequence_number
    poc_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parsers.parse_incoming_message(fields, message)
    ack_bytes = generators.generate_ack_message(fields, poc_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(ack_bytes)
    #
    conn.send(ack_bytes)
    return fields


def answer_observations(conn, message):
    global poc_sequence_number
    poc_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parsers.parse_incoming_message(fields, message)
    ack_bytes = generators.generate_ack_message(fields, poc_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(ack_bytes)
    #
    conn.send(ack_bytes)
    return fields


def request_observations(conn, fields):
    global poc_sequence_number
    poc_sequence_number += 1
    request_bytes = generators.generate_request4observations_message(fields, poc_sequence_number)
    #
    print("----------------------------")
    print("[REQ.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(request_bytes)
    #
    conn.send(request_bytes)


def start_continuous_directive(conn, fields):
    global poc_sequence_number
    poc_sequence_number += 1
    request_bytes = generators.generate_cont_directive_message(fields, poc_sequence_number)
    #
    print("----------------------------")
    print("[DTV.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(request_bytes)
    #
    conn.send(request_bytes)


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
                    #
                    print("----------------------------")
                    print("DCA => [HEL.R01]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #
                    answer_hello(conn, data_str)

                elif "DST.R01" in data_str:
                    #
                    print("----------------------------")
                    print("DCA => [DST.R01]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #
                    _fields = answer_device_status(conn, data_str)
                    request_observations(conn, _fields)

                elif "OBS.R01" in data_str:
                    #
                    print("----------------------------")
                    print("DCA => [OBS.R01]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #
                    answer_observations(conn, data_str) 

                elif "EOT.R01" in data_str:
                    #
                    print("----------------------------")
                    print("DCA => [EOT.R01]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #
                    fields = {
                            "control_id" : "",
                            "creation_dttm" : "",
                    }
                    parsers.parse_incoming_message(fields, data_str)
                    start_continuous_directive(conn, fields)

                elif "ACK.R01" in data_str:
                    #
                    print("----------------------------")
                    print("DCA => [ACK.R01]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #
                    print("----------------------------")
                    print("BASIC PROFILE CONVERSATION FLOW COMPLETED!")
                    print("----------------------------")
                    

                elif "ESC.R01" in data_str and "OTH" in data_str:
                    raise Exception("!!!BAD ACK!!!")

                else:
                    #
                    print("----------------------------")
                    print("DCA => [???]")
                    print("----------------------------")
                    parsers.prettyprint(data)
                    #

    except Exception as e:
        print("ERROR: {}".format(e))
        track = traceback.format_exc()
        print(track)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        sock.close()
