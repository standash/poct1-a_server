import parsers 
import generators
from poct1_server import own_sequence_number


def ack_message(conn, message):
    global own_sequence_number
    own_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parsers.parse_incoming_message(fields, message)
    device_sequence_number = fields["control_id"]
    latest_timestamp = fields["creation_dttm"]
    _bytes = generators.generate_ack_message(latest_timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)
    return fields


def end_of_topic_message(conn, message):
    global own_sequence_number
    own_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parsers.parse_incoming_message(fields, message)
    device_sequence_number = fields["control_id"]
    latest_timestamp = fields["creation_dttm"]
    _bytes = generators.generate_end_of_topic_message(latest_timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[EOT.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)
    return fields


def request_observations(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    _bytes = generators.generate_request4observations_message(latest_timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[REQ.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)


def start_continuous_directive(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    _bytes = generators.generate_cont_directive_message(latest_timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[DTV.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)


def update_operator_list(latest_timestamp, operator_name, operator_password, conn):
    global own_sequence_number
    own_sequence_number += 1
    _bytes = generators.generate_operator_list_update_message(latest_timestamp, own_sequence_number, operator_name, operator_password)
    #
    print("----------------------------")
    print("[OPL.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)


def send_remote_command(latest_timestamp, command, conn):
    global own_sequence_number
    own_sequence_number += 1
    _bytes = generators.generate_remote_command_message(latest_timestamp, own_sequence_number, command)
    #
    print("----------------------------")
    print("[DTV.SIEM.DVCMD] ({}) => DCA".format(command))
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)


def terminate_conversation(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    _bytes = generators.generate_terminate_message(latest_timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[END.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(_bytes)
    #
    conn.send(_bytes)


def terminate_conversation_flow(latest_timestamp, conn):
    terminate_conversation(latest_timestamp, conn)
    latest_timestamp = None
    while True:
        data = conn.recv(1024)
        if not data:
            raise Exception("NO DATA FROM DEVICE!")
        data_str = data.strip().decode("utf-8")
        if "ACK.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            print("----------------------------")
            print("END OF CONVERSATION")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
    return latest_timestamp


def send_remote_command_flow(latest_timestamp, command, conn):
    send_remote_command(latest_timestamp, command, conn)
    latest_timestamp = None
    while True:
        data = conn.recv(1024)
        if not data:
            raise Exception("NO DATA FROM DEVICE!")

        data_str = data.strip().decode("utf-8")
        if "ACK.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            print("----------------------------")
            print("REMOTE COMMAND HAS BEEN EXECUTED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        elif "ESC.R01" in data_str and "CNC" in data_str:
            #
            print("----------------------------")
            print("DCA => [ESC.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            print("----------------------------")
            print("SYSTEM IS BUSY, REMOTE COMMAND FAILED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        #----------------------------------------------------
        else:
            #
            print("----------------------------")
            print("DCA => [???]")
            print("----------------------------")
            parsers.prettyprint(data)
    
    return latest_timestamp


def update_operators_list_flow(latest_timestamp, name, password, conn):
    update_operator_list(latest_timestamp, name, password, conn)
    operator_updated = False
    latest_timestamp = None
    while True:
        data = conn.recv(1024)
        if not data:
            raise Exception("NO DATA FROM DEVICE!")

        data_str = data.strip().decode("utf-8")
        if "ACK.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            if operator_updated:
                print("----------------------------")
                print("OPERATOR LIST HAS BEEN UPDATED")
                print("----------------------------")
                fields = {
                        "creation_dttm" : "",
                }
                parsers.parse_incoming_message(fields, data_str)
                latest_timestamp = fields["creation_dttm"]
                break
            else:
                end_of_topic_message(conn, data_str)

        elif "EVS.R01" in data_str and "Operator List Update Succeeded" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            operator_updated = True

        elif "ESC.R01" in data_str and "CNC" in data_str:
            #
            print("----------------------------")
            print("DCA => [ESC.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            print("----------------------------")
            print("SYSTEM IS BUSY, OPERATOR LIST UPDATE FAILED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        #----------------------------------------------------
        else:
            #
            print("----------------------------")
            print("DCA => [???]")
            print("----------------------------")
            parsers.prettyprint(data)
    return latest_timestamp



def basic_conversation_flow(conn):
    latest_timestamp = None
    while True:
        data = conn.recv(1024)
        if not data:
            raise Exception("NO DATA FROM DEVICE!")

        data_str = data.strip().decode("utf-8")
        if "HEL.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [HEL.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            ack_message(conn, data_str)

        elif "DST.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [DST.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            fields = ack_message(conn, data_str)
            request_observations(fields["creation_dttm"], conn)

        elif "OBS.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [OBS.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            ack_message(conn, data_str) 

        elif "EOT.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [EOT.R01]")
            print("----------------------------")
            parsers.prettyprint(data)
            #
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            start_continuous_directive(fields["creation_dttm"], conn)

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
            fields = {
                    "creation_dttm" : "",
            }
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break

        elif "ESC.R01" in data_str and "OTH" in data_str:
            raise Exception("DCA => !!!BAD ACK!!! \n{}".format(parsers.prettyprint(data)))
        else:
            raise Exception("DCA => !!!UNEXPECTED MESSAGE!!! \n{}".format(parsers.prettyprint(data)))
    return latest_timestamp
