import parsers 
import generators
from poct1_server import own_sequence_number

# TODO: EVS.R01
#       -> device events
#       -> operator list update?

# TODO: OBS.R02
#       -> non-patient observations

# TODO: DTV.SIEM.DVCMD
#       -> remote commend directive

# TODO: KPA.R01
#       -> keep alive message

# TODO: KPA.R01
#       -> keep alive message

# TODO: END.R01
#       -> terminate message

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
    ack_bytes = generators.generate_ack_message(latest_timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(ack_bytes)
    #
    conn.send(ack_bytes)
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
    eot_bytes = generators.generate_end_of_topic_message(latest_timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[EOT.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(eot_bytes)
    #
    conn.send(eot_bytes)
    return fields



def request_observations(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    request_bytes = generators.generate_request4observations_message(latest_timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[REQ.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(request_bytes)
    #
    conn.send(request_bytes)


def start_continuous_directive(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    request_bytes = generators.generate_cont_directive_message(latest_timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[DTV.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(request_bytes)
    #
    conn.send(request_bytes)


def update_operator_list(latest_timestamp, operator_name, operator_password, conn):
    global own_sequence_number
    own_sequence_number += 1
    request_bytes = generators.generate_operator_list_update_message(latest_timestamp, own_sequence_number, operator_name, operator_password)
    #
    print("----------------------------")
    print("[OPL.R01] => DCA")
    print("----------------------------")
    parsers.prettyprint(request_bytes)
    #
    conn.send(request_bytes)


def update_operators_list_flow(latest_timestamp, name, password, conn):
    operator_updated = False
    update_operator_list(latest_timestamp, name, password, conn)
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
            break
        #----------------------------------------------------
        else:
            #
            print("----------------------------")
            print("DCA => [???]")
            print("----------------------------")
            parsers.prettyprint(data)



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
            parsers.parse_incoming_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break

        elif "ESC.R01" in data_str and "OTH" in data_str:
            raise Exception("DCA => !!!BAD ACK!!! \n{}".format(parsers.prettyprint(data)))
        else:
            raise Exception("DCA => !!!UNEXPECTED MESSAGE!!! \n{}".format(parsers.prettyprint(data)))
    return latest_timestamp
