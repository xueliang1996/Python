

import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


app = Flask(__name__)
@app.route('/getSessionID_hash',methods=['GET'])

def getSessionID_hash():
    url = 'http://120.26.202.123/jinlang_channels/index.php?m=index&c=login&a=check_login'
    UA = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'

    header = {"User-Agent": UA,
              "Referer": url
              }
    JLsession = requests.Session()

    form= {'username': 'QDmaiju@126.com',
                'password': 'mj258123',
                'dosubmit': ''
                }

    JLsession.post(url, data=form, headers=header)
    f = JLsession.get('http://120.26.202.123/jinlang_channels/index.php?m=index&c=index&member_hash=PtlasO',
                      headers=header)
    f.encoding = 'utf-8'
    soup = BeautifulSoup(f.text, "html.parser")
    hash_code = soup.find_all("a")[1].attrs
    str = hash_code.get("href")
    index = str.index("member_hash=")
    hash = str[index + 12:]
    cookies = JLsession.cookies
    sessionID = cookies.get('PHPSESSID')
    return jsonify({'sessionID':sessionID,'hash':hash})

app.run(host='192.168.1.126',port=80443)
