import base64
import os
import help

database = help.openDB()
conn = database[0]
cur = database[1]

cur.execute("select base64 from pic_18510363933_artificial where cultivar_id = 2 and pic_type = '5'")
conn.commit()
result = cur.fetchall()
base64str = result[0][0]
print(base64str)

# with open('G:\\mum_pic\\artificial\\processed\\18510363933@163.com\\2\\2太真图-1.JPG', 'rb') as f:
#     base64str = base64.b64encode(f.read())
#     print(base64str)
#     # base64str += '=' *  missing_padding
#     imgdata = base64.b64decode(base64str)
#     file = open("G:\\1.JPG", 'wb')
#     file.write(imgdata)
#     file.close()
#     print(base64str)


# lens = len(base64str)
# lenx = lens - (lens % 4 if lens % 4 else 4)
# missing_padding = 4 - len(base64str) % 4
# if missing_padding:
#     base64str += '=' *  missing_padding
imgdata = base64.b64decode(base64str)
file = open("G:\\1.JPG", 'wb')
file.write(imgdata)
file.close()