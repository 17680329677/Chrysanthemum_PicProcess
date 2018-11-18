import nsq
import help
from ArtificialPic import artificial_pic
from Email import packAndSend
from InstrumentPic import instrument_pic, instrument_pack

nsq_conf = help.read_conf(help.getRoot() + '/config/dataConfig.json')['nsq']
heartbeat = 36
max_tries = 1

artificial_process = nsq.Reader(
    message_handler=artificial_pic.artificial_pic_process,
    nsqd_tcp_addresses=[nsq_conf['host'] + ":" + nsq_conf['port']],
    topic='artificialPicProcess', channel='channel',
    lookupd_poll_interval=15,
    max_tries=max_tries, heartbeat_interval=heartbeat
)

send_email = nsq.Reader(
    message_handler=packAndSend.packAndSend,
    nsqd_tcp_addresses=[nsq_conf['host'] + ":" + nsq_conf['port']],
    topic='sendEmail', channel='channel',
    lookupd_poll_interval=15,
    max_tries=max_tries, heartbeat_interval=heartbeat
)

instrumentOriginPicProcess = nsq.Reader(
    message_handler=instrument_pic.origin_process,
    nsqd_tcp_addresses=[nsq_conf['host'] + ":" + nsq_conf['port']],
    topic='instrumentOriginPicProcess', channel='channel',
    lookupd_poll_interval=15,
    max_tries=max_tries, heartbeat_interval=heartbeat
)

instrumentProPicProcess = nsq.Reader(
    message_handler=instrument_pic.pro_process,
    nsqd_tcp_addresses=[nsq_conf['host'] + ":" + nsq_conf['port']],
    topic='instrumentProPicProcess', channel='channel',
    lookupd_poll_interval=15,
    max_tries=max_tries, heartbeat_interval=heartbeat
)

instrumentPack = nsq.Reader(
    message_handler=instrument_pack.pack,
    nsqd_tcp_addresses=[nsq_conf['host'] + ":" + nsq_conf['port']],
    topic='instrumentPack', channel='channel',
    lookupd_poll_interval=15,
    max_tries=max_tries, heartbeat_interval=heartbeat
)

print("pic process 0.2")
nsq.run()
