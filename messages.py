import base64
from datetime import datetime

ack_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<ACK.R01>
<HDR>
<HDR.message_type V=\"ACK.R01\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<ACK>
<ACK.type_cd V=\"AA\"/>
<ACK.ack_control_id V=\"{}\" />
</ACK>
</ACK.R01>
"""

obs_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<REQ.R01>
<HDR>
<HDR.message_type V=\"REQ.R01\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<REQ>
<REQ.request_cd V=\"ROBS\" />
</REQ>
</REQ.R01>
"""

dtv_cont_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<DTV.R01>
<HDR>
<HDR.message_type V=\"DTV.R01\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<DTV>
<DTV.command_cd V=\"START_CONTINUOUS\"  />
</DTV>
</DTV.R01>
"""

opl_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<OPL.R01>
<HDR>
<HDR.message_type V=\"OPL.R01\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<OPR>
<OPR.operator_id V=\"{}\" />
<ACC>
<ACC.method_cd V=\"ALL\" />
<ACC.password ENC=\"B64\">{}</ACC.password>
<ACC.permission_level_cd V=\"1\" />
</ACC>
</OPR>
</OPL.R01>
"""

eot_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<EOT.R01>
<HDR>
<HDR.message_type V=\"EOT.R01\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<EOT>
<EOT.topic_cd V=\"OPL\" />
<EOT.eot_control_id V=\"{}\" />
</EOT>
</EOT.R01>
"""

dtv_siem_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<DTV.SIEM.DVCMD>
<HDR>
<HDR.message_type V=\"DTV.SIEM.DVCMD\" SN=\"SIEM\" SV=\"1.0\" />
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<DTV>
<DTV.command_cd V=\"{}\" SN=\"SIEM\" SV=\"1.0\" />
</DTV>
</DTV.SIEM.DVCMD>
"""

end_msg = """
<?xml version=\"1.0\" encoding=\"utf-8\"?>
<END.R01>
<HDR>
<HDR.control_id V=\"{}\"/>
<HDR.version_id V=\"POCT1\" />
<HDR.creation_dttm V=\"{}\" />
</HDR>
<TRM>
<TRM.reason_cd V=\"UNK\" />
</TRM>
</END.R01>
"""

def prepare_ack_msg(timestamp, own_seq_num, dev_seq_num):
    msg = ack_msg.format(own_seq_num, timestamp, dev_seq_num)
    return msg.replace("\n", "").encode("utf-8")
    

def prepare_eot_msg(timestamp, own_seq_num, dev_seq_num):
    msg = eot_msg.format(own_seq_num, timestamp, dev_seq_num)
    return msg.replace("\n", "").encode("utf-8")


def prepare_obs_msg(timestamp, own_seq_num):
    msg = obs_msg.format(own_seq_num, timestamp)
    return msg.replace("\n", "").encode("utf-8")


def prepare_dtv_cont_msg(timestamp, own_seq_num):
    msg = dtv_cont_msg.format(own_seq_num, timestamp)
    return msg.replace("\n", "").encode("utf-8")


def prepare_opl_msg(timestamp, own_seq_num, operator_id, operator_password):
    base64_password = base64.b64encode(operator_password.encode("utf-8")).decode("utf-8")
    msg = opl_msg.format(own_seq_num, timestamp, operator_id, base64_password)
    return msg.replace("\n", "").encode("utf-8")


def prepare_dtv_siem_msg(timestamp, own_seq_num, command):
    msg = dtv_siem_msg.format(own_seq_num, timestamp, command)
    return msg.replace("\n", "").encode("utf-8")

