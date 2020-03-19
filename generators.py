import base64
from datetime import datetime
from dateutil.relativedelta import * 


def generate_ack_message(latest_timestamp, own_seq_num, device_seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<ACK.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"ACK.R01\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<ACK>".encode("utf-8")
    bytez += "<ACK.type_cd V=\"AA\"/>".encode("utf-8")
    bytez += "<ACK.ack_control_id V=\"{}\" />".format(device_seq_num).encode("utf-8")
    bytez += "</ACK>".encode("utf-8")
    bytez += "</ACK.R01>".encode("utf-8")
    return bytez


def generate_request4observations_message(latest_timestamp, own_seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<REQ.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"REQ.R01\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<REQ>".encode("utf-8")
    bytez += "<REQ.request_cd V=\"ROBS\" />".encode("utf-8")
    bytez += "</REQ>".encode("utf-8")
    bytez += "</REQ.R01>".encode("utf-8")
    return bytez


def generate_cont_directive_message(latest_timestamp, own_seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<DTV.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"DTV.R01\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<DTV>".encode("utf-8")
    bytez += "<DTV.command_cd V=\"START_CONTINUOUS\"  />".encode("utf-8")
    bytez += "</DTV>".encode("utf-8")
    bytez += "</DTV.R01>".encode("utf-8")
    return bytez


def generate_operator_list_update_message(latest_timestamp, own_seq_num, operator_name, operator_password):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<OPL.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"OPL.R01\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<OPR>".encode("utf-8")
    bytez += "<OPR.operator_id V=\"{}\" />".format(operator_name).encode("utf-8")
    bytez += "<ACC>".encode("utf-8")
    bytez += "<ACC.method_cd V=\"ALL\" />".encode("utf-8")
    #
    base64_password = base64.b64encode(operator_password.encode("utf-8")).decode("utf-8")
    bytez += "<ACC.password ENC=\"B64\">{}</ACC.password>".format(base64_password).encode("utf-8")
    #
    bytez += "<ACC.permission_level_cd V=\"1\" />".encode("utf-8")
    bytez += "</ACC>".encode("utf-8")
    bytez += "</OPR>".encode("utf-8")
    bytez += "</OPL.R01>".encode("utf-8")
    return bytez


def generate_end_of_topic_message(latest_timestamp, own_seq_num, device_seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<EOT.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"EOT.R01\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<EOT>".encode("utf-8")
    bytez += "<EOT.topic_cd V=\"OPL\" />".encode("utf-8")
    bytez += "<EOT.eot_control_id V=\"{}\" />".format(device_seq_num).encode("utf-8")
    bytez += "</EOT>".encode("utf-8")
    bytez += "</EOT.R01>".encode("utf-8")
    return bytez


def generate_remote_command_message(latest_timestamp, own_seq_num, command):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<DTV.SIEM.DVCMD>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.message_type V=\"DTV.SIEM.DVCMD\" SN=\"SIEM\" SV=\"1.0\" />".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<DTV>".encode("utf-8")
    bytez += "<DTV.command_cd V=\"{}\" SN=\"SIEM\" SV=\"1.0\" />".format(command).encode("utf-8")
    bytez += "</DTV>".encode("utf-8")
    bytez += "</DTV.SIEM.DVCMD>".encode("utf-8")
    return bytez


def generate_terminate_message(latest_timestamp, own_seq_num):
    bytez = b""
    bytez += "<?xml version=\"1.0\" encoding=\"utf-8\"?>".encode("utf-8")
    bytez += "<END.R01>".encode("utf-8")
    bytez += "<HDR>".encode("utf-8")
    bytez += "<HDR.control_id V=\"{}\"/>".format(own_seq_num).encode("utf-8")
    bytez += "<HDR.version_id V=\"POCT1\" />".encode("utf-8")
    #
    timestamp = increment_timestamp(latest_timestamp, 1)
    bytez += "<HDR.creation_dttm V=\"{}\" />".format(timestamp).encode("utf-8")
    #
    bytez += "</HDR>".encode("utf-8")
    bytez += "<TRM>".encode("utf-8")
    bytez += "<TRM.reason_cd V=\"UNK\" />".encode("utf-8")
    bytez += "</TRM>".encode("utf-8")
    bytez += "</END.R01>".encode("utf-8")
    return bytez



def increment_timestamp(timestamp, n_seconds):
    chunks = timestamp.split("-")
    xxx = chunks[2].split("T")
    time = datetime.strptime(xxx[1], "%H:%M:%S")
    time = time + relativedelta(seconds = n_seconds)
    return "{}-{}-{}T{}-{}".format(chunks[0], chunks[1], xxx[0], time.strftime("%H:%M:%S"), chunks[3])

