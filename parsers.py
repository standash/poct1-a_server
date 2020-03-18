import xml.dom.minidom
import xml.etree.ElementTree as ET


def prettyprint(bytez):
    s = bytez.decode("utf-8")
    dom = xml.dom.minidom.parseString(s)
    print(dom.toprettyxml())


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
