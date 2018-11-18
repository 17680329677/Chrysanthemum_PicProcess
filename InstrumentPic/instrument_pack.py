import os
import json
import help
import pandas as pd
import shutil
from datetime import datetime


def pack(message):
    msg = message.body.decode()
    email = json.loads(msg).get('email', None)
    ids = json.loads(msg).get('ids', None)

    if ids:
        database = help.openDB()
        conn = database[0]
        cur = database[1]
        origins = []
        for id in ids:
            cur.execute("select * from instrument_origin_pictures where id = %s", (id,))
            origin = cur.fetchall()
            origins.append(origin[0])

    help.save_redis(email.split('@')[0] + '_pack', json.dumps({
        'status': 'success',
        'reason': 'instrument data pack finished!'
    }))
    return True