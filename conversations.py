import parsers 
import generators
from poct1_server import own_sequence_number

# TODO: OPS.R01
#       -> The data manager can create a new operator list for the DCA Vantage Analyzer by sending a Complete Update message (OPL.R01).
#       -> operator list download?

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


def update_operators_list_flow(conn):
    pass


def basic_conversation_flow(conn):
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
            break

        elif "ESC.R01" in data_str and "OTH" in data_str:
            raise Exception("DCA => !!!BAD ACK!!! \n{}".format(parsers.prettyprint(data)))
        else:
            raise Exception("DCA => !!!UNEXPECTED MESSAGE!!! \n{}".format(parsers.prettyprint(data)))
