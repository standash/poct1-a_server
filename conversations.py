import base64
import messages
import xml.dom.minidom
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil.relativedelta import * 

own_sequence_number = 4000

def prettyprint(bytez):
    s = bytez.decode("utf-8")
    dom = xml.dom.minidom.parseString(s)
    print(dom.toprettyxml())


def parse_xml(fields, xml_element):
    if xml_element == None:
        return
    for key in fields:
        if fields[key] == "" and key in xml_element.tag:
            fields[key] = xml_element.attrib["V"]
    for xml_child in list(xml_element):
        parse_xml(fields, xml_child)


def parse_received_message(fields, message):
    xml_root = ET.fromstring(message)
    parse_xml(fields, xml_root)


def increment_timestamp(timestamp, n_seconds):
    chunks = timestamp.split("-")
    xxx = chunks[2].split("T")
    time = datetime.strptime(xxx[1], "%H:%M:%S")
    time = time + relativedelta(seconds = n_seconds)
    return "{}-{}-{}T{}-{}".format(chunks[0], chunks[1], xxx[0], time.strftime("%H:%M:%S"), chunks[3])


def send_ack_message(conn, message):
    global own_sequence_number
    own_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parse_received_message(fields, message)
    device_sequence_number = fields["control_id"]
    latest_timestamp = fields["creation_dttm"]
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_ack_msg(timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[ACK.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)
    return fields


def send_request_observations(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_obs_msg(timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[REQ.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)


def send_start_continuous_directive(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_dtv_cont_msg(timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[DTV.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)

def send_start_continuous_directive(latest_timestamp, conn):
    global own_sequence_number
    own_sequence_number += 1
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_dtv_cont_msg(timestamp, own_sequence_number)
    #
    print("----------------------------")
    print("[DTV.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)


def send_end_of_topic_message(conn, message):
    global own_sequence_number
    own_sequence_number += 1
    fields = {
            "control_id" : "",
            "creation_dttm" : "",
    }
    parse_received_message(fields, message)
    device_sequence_number = fields["control_id"]
    latest_timestamp = fields["creation_dttm"]
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_eot_msg(timestamp, own_sequence_number, device_sequence_number)
    #
    print("----------------------------")
    print("[EOT.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)
    return fields


def update_operator_list(latest_timestamp, operator_name, operator_password, conn):
    global own_sequence_number
    own_sequence_number += 1
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_opl_msg(timestamp, own_sequence_number, operator_name, operator_password)
    #
    print("----------------------------")
    print("[OPL.R01] => DCA")
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)


def send_remote_command(latest_timestamp, command, conn):
    global own_sequence_number
    own_sequence_number += 1
    timestamp = increment_timestamp(latest_timestamp, 1)
    _bytes = messages.prepare_dtv_siem_msg(timestamp, own_sequence_number, command)
    print("----------------------------")
    print("[DTV.SIEM.DVCMD] ({}) => DCA".format(command))
    print("----------------------------")
    prettyprint(_bytes)
    #
    conn.send(_bytes)


def remote_command_flow(latest_timestamp, command, conn):
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
            prettyprint(data)
            #
            print("----------------------------")
            print("REMOTE COMMAND HAS BEEN EXECUTED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parse_received_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        elif "ESC.R01" in data_str and "CNC" in data_str:
            #
            print("----------------------------")
            print("DCA => [ESC.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            print("----------------------------")
            print("SYSTEM IS BUSY, REMOTE COMMAND FAILED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parse_received_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        #----------------------------------------------------
        else:
            #
            print("----------------------------")
            print("DCA => [???]")
            print("----------------------------")
            prettyprint(data)
    
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
            prettyprint(data)
            #
            if operator_updated:
                print("----------------------------")
                print("OPERATOR LIST HAS BEEN UPDATED")
                print("----------------------------")
                fields = {
                        "creation_dttm" : "",
                }
                parse_received_message(fields, data_str)
                latest_timestamp = fields["creation_dttm"]
                break
            else:
                send_end_of_topic_message(conn, data_str)

        elif "EVS.R01" in data_str and "Operator List Update Succeeded" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            operator_updated = True

        elif "ESC.R01" in data_str and "CNC" in data_str:
            #
            print("----------------------------")
            print("DCA => [ESC.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            print("----------------------------")
            print("SYSTEM IS BUSY, OPERATOR LIST UPDATE FAILED")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parse_received_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break
        #----------------------------------------------------
        else:
            #
            print("----------------------------")
            print("DCA => [???]")
            print("----------------------------")
            prettyprint(data)
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
            prettyprint(data)
            #
            send_ack_message(conn, data_str)

        elif "DST.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [DST.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            fields = send_ack_message(conn, data_str)
            send_request_observations(fields["creation_dttm"], conn)


        elif "OBS.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [OBS.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            send_ack_message(conn, data_str) 

        elif "EOT.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [EOT.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            fields = {
                    "creation_dttm" : "",
            }
            parse_received_message(fields, data_str)
            send_start_continuous_directive(fields["creation_dttm"], conn)

        elif "ACK.R01" in data_str:
            #
            print("----------------------------")
            print("DCA => [ACK.R01]")
            print("----------------------------")
            prettyprint(data)
            #
            print("----------------------------")
            print("BASIC PROFILE CONVERSATION FLOW COMPLETED!")
            print("----------------------------")
            fields = {
                    "creation_dttm" : "",
            }
            parse_received_message(fields, data_str)
            latest_timestamp = fields["creation_dttm"]
            break

        elif "ESC.R01" in data_str and "OTH" in data_str:
            prettyprint(data)
            raise Exception("DCA => !!!BAD ACK!!!")
        else:
            prettyprint(data)
            raise Exception("DCA => !!!UNEXPECTED MESSAGE!!!")
    return latest_timestamp
