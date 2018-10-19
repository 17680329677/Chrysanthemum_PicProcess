import nsq
import help
from ArtificialPic import artificial_pic

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


print("pic process 0.1")
nsq.run()
