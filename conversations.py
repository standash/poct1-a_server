import parsers 
import generators
from poct1_server import poc_sequence_number

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


def basic_conversation_flow(conn):
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
            break

        elif "ESC.R01" in data_str and "OTH" in data_str:
            raise Exception("DCA => !!!BAD ACK!!! \n{}".format(parsers.prettyprint(data)))
        else:
            raise Exception("DCA => !!!UNEXPECTED MESSAGE!!! \n{}".format(parsers.prettyprint(data)))
