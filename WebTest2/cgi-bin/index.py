#!/usr/bin/env python3
# -*- coding: utf-8 -*-

html = '''Content-type: text/html;


<html>
<head>
  <meta http-equiv="Content-Type" content="text/html" charset="UTF-8" />
  <title>ファイルをアップロードする</title>
</head>
<body>
<h1>ファイルをアップロードする</h1>
<p>%s</p>
<p>%s</p>
<form action="index.py" method="post" enctype="multipart/form-data">
  <input type="file" name="file" />
  <input type="submit" />
</form>
</body>
</html>
'''

import cgi
import os, sys
import numpy as np
import pandas as pd
from aip import AipImageClassify

""" 你的 APPID AK SK """
APP_ID = '24555716'
API_KEY = 'A6hcfZTTExXetYuPCgq0Cldi'
SECRET_KEY = 'qUweXzyGyy3gqTZ4HPEKKC1TeIR8xiDI'

client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)

try:
    import msvcrt
    msvcrt.setmode(0, os.O_BINARY)
    msvcrt.setmode(1, os.O_BINARY)
except ImportError:
    pass

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

content=''
content2=''
files=[]
form = cgi.FieldStorage()
if 'file' in form:
    item = form['file']
    if item.file:
        fout = open(os.path.join('./img/', item.filename), 'wb')
        while True:
            chunk = item.file.read(1000000)
            if not chunk:
                break
            fout.write(chunk)
        fout.close()

    # /cgi-bin/tmpが置かれている場所を指定
    filepath='../img/'+item.filename

    filepath2='/Users/lilina/Downloads/WebTest2/img/'+item.filename

    image = get_file_content(filepath2)

    content=client.advancedGeneral(image)
    content2='<img src="'+filepath+'" width="50%" height="auto">'

print (html % (content,content2))