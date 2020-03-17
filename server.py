#!/usr/bin/env python3

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


    def handle_hello_message(self, message):
        print("Received HELLO message")
        template = {
                "message_type" : "",
                "device_id" : "",
                "control_id" : "",
                "version_id" : "",
        }
        xml_root = ET.fromstring(message)
        self.parse_xml(xml_root, template)
        print(template)

    def print_msg(self):
        print("{} wrote:\n".format(self.client_address[0]))
        print(self.data)
        print("")


    def handle(self):
        self.data = self.request.recv(1024).strip()
        # ------------------------------------------------
        self.print_msg()
        # ------------------------------------------------
        data_str = self.data.decode("latin-1")
        if "HEL.R01" in data_str:
            self.handle_hello_message(data_str)
        else:
            pass



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
