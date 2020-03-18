from datetime import datetime
from dateutil.relativedelta import * 


def generate_ack_message(msg, seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<ACK.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"ACK.R01\" />".encode("utf-8")
    #
    new_control_id = str(int(msg["control_id"]) + 1)
    bytez += "<HDR.control_id V=\"{}\"/>".format(seq_num).encode("utf-8")
    #
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(msg["creation_dttm"], 2)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<ACK>".encode("utf-8")
    bytez += "<ACK.type_cd V=\"AA\"/>".encode("utf-8")
    bytez += "<ACK.ack_control_id V=\"{}\" />".format(msg["control_id"]).encode("utf-8")
    bytez += "</ACK>".encode("utf-8")
    bytez += "</ACK.R01>".encode("utf-8")
    return bytez


def increment_timestamp(timestamp, n_seconds):
    chunks = timestamp.split("-")
    xxx = chunks[2].split("T")
    time = datetime.strptime(xxx[1], "%H:%M:%S")
    time = time + relativedelta(seconds = n_seconds)
    return "{}-{}-{}T{}-{}".format(chunks[0], chunks[1], xxx[0], time.strftime("%H:%M:%S"), chunks[3])

