#!/usr/bin/env python3

import sys
import socketserver
import xml.etree.ElementTree as ET

poc_host, poc_port = "192.168.2.100", 3001


class POCT1Handler(socketserver.BaseRequestHandler):

    def parse_xml(self, xml_element, template):
        if xml_element == None:
            return
        for key in template:
            if template[key] == "" and key in xml_element.tag:
                template[key] = xml_element.attrib["V"]
        for xml_child in list(xml_element):
            self.parse_xml(xml_child, template)


    def parse_hello_message(self, message):
        print("Received HELLO message")
        msg = {
                "message_type" : "",
                "device_id" : "",
                "control_id" : "",
                "creation_dttm" : "",
                "version_id" : "",
        }
        xml_root = ET.fromstring(message)
        self.parse_xml(xml_root, msg)
        return msg

    def generate_ack_message(self, msg):
        ############################################
        with open("dummy_response.xml", "r") as _f:
            xml = _f.read()
        ack_msg = "".join(xml.split())
        ack_msg = ack_msg.rstrip("\x0a")
        ############################################
        control_id = msg["control_id"]
        creation_dttm = msg["creation_dttm"]
        ack_msg = ack_msg.replace("##CONTROLID##", control_id)
        ack_msg = ack_msg.replace("##TIMESTAMP##", creation_dttm)
        return ack_msg

    def handle(self):
        # keep the connection open until client terminates
        while True:
            self.data = self.request.recv(1024)
            if not self.data:
                break

            data_str = self.data.strip().decode("utf-8")
            if "HEL.R01" in data_str:
                print("DCA => [HELLO]")
                hello_msg = self.parse_hello_message(data_str)
                ack_msg = self.generate_ack_message(hello_msg)
                ack_bytes = ack_msg.encode("utf-8")
                self.request.sendall(ack_bytes)
                print("[ACK] => DCA")
            elif "ESC.R01" in data_str and "OTH" in data_str:
                print("!!!BAD ACK!!!")
                break
            else:
                print(self.data)


if __name__ == "__main__":
    # ------------------------------------------------
    socketserver.TCPServer.allow_reuse_address = True
    server = None
    # ------------------------------------------------
    try:
        server = socketserver.TCPServer((poc_host, poc_port), POCT1Handler) 
        server.serve_forever()
    except KeyboardInterrupt:
        print("Stopped the server")
    finally:
        if server != None:
            server.shutdown()
            server.server_close()
