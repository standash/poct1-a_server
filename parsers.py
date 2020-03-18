import xml.dom.minidom
import xml.etree.ElementTree as ET


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


def parse_incoming_message(fields, message):
    xml_root = ET.fromstring(message)
    parse_xml(fields, xml_root)
