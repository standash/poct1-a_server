#!/usr/bin/env python3

import sys
import socket
import xml.etree.ElementTree as ET
from datetime import datetime
from dateutil.relativedelta import *
import xml.dom.minidom

poc_host, poc_port = "192.168.2.100", 3001

def prettyprint(bytez):
    s = bytez.decode("utf-8")
    dom = xml.dom.minidom.parseString(s)
    print(dom.toprettyxml())

def increment_timestamp(timestamp, n_seconds):
    chunks = timestamp.split("-")
    xxx = chunks[2].split("T")
    time = datetime.strptime(xxx[1], "%H:%M:%S")
    time = time + relativedelta(seconds = n_seconds)
    return "{}-{}-{}T{}-{}".format(chunks[0], chunks[1], xxx[0], time.strftime("%H:%M:%S"), chunks[3])


def parse_xml(xml_element, template):
    if xml_element == None:
        return
    for key in template:
        if template[key] == "" and key in xml_element.tag:
            template[key] = xml_element.attrib["V"]
    for xml_child in list(xml_element):
        parse_xml(xml_child, template)


def parse_hello_message(message):
    msg = {
            "message_type" : "",
            "device_id" : "",
            "control_id" : "",
            "creation_dttm" : "",
            "version_id" : "",
    }
    xml_root = ET.fromstring(message)
    parse_xml(xml_root, msg)
    return msg

def generate_ack_message(msg):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")

    bytez += "<ACK.R01>".encode("utf-8")

    bytez += "<HDR>".encode("utf-8")

    bytez += "<HDR.message_type V=\"ACK.R01\" />".encode("utf-8")

    new_control_id = str(int(msg["control_id"]) + 1)
    bytez += "<HDR.control_id V=\"{}\"/>".format("4001").encode("utf-8")

    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")

    timestamp = increment_timestamp(msg["creation_dttm"], 2)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")

    bytez += "</HDR>".encode("utf-8")

    bytez += "<ACK>".encode("utf-8")

    bytez += "<ACK.type_cd V=\"AA\"/>".encode("utf-8")

    bytez += "<ACK.ack_control_id V=\"{}\" />".format(msg["control_id"]).encode("utf-8")

    bytez += "</ACK>".encode("utf-8")

    bytez += "</ACK.R01>".encode("utf-8")

    return bytez


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
                    print("DCA => [HELLO]\n")
                    prettyprint(data)

                    hello_msg = parse_hello_message(data_str)
                    ack_bytes = generate_ack_message(hello_msg)
                    conn.send(ack_bytes)

                    print("[ACK] => DCA\n")
                    prettyprint(ack_bytes)
                elif "ESC.R01" in data_str and "OTH" in data_str:
                    print("!!!BAD ACK!!!")
                    # raise Exception("!!!BAD ACK!!!")
                else:
                    print("DCA => [???]\n")
                    prettyprint(data)
            sock.close()
    except Exception as e:
        print("ERROR: {}".format(e))
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        sock.close()
