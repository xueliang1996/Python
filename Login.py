import configparser
import time
import re
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, make_response



# 配置信息
cf = configparser.ConfigParser()
cf.read('pythonConf.ini', encoding='utf-8')
IP = cf.get('config', 'IP')
port = int(cf.get('config', 'port'))

url = 'http://www.tianmasport.com/ms/login.shtml'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

header = {"User-Agent": UA,
          "Referer": url
          }


def simLogin():
    codeUrl = 'http://www.tianmasport.com/ms/ImageServlet?time=new%20Date().getTime()'
    valcode = requests.get(codeUrl)
    checkCookie = requests.utils.dict_from_cookiejar(valcode.cookies)
    f = open('valcode.jpg', 'wb')
    f.write(valcode.content)
    f.close()
    time.sleep(1)
    # 获取验证码
    vcode = input('请输入验证码：'),
    # 读取配置信息
    cf = configparser.ConfigParser()
    cf.read('config.ini', encoding='utf-8')
    nickName = cf.get('config', 'nickName')
    pwd = cf.get('config', 'pwd')
    # 模拟登陆
    form = {'nickName': nickName,
            'pwd': pwd,
            'verifyCode': vcode,
            'remember': 'on'
            }
    # 如果不进fUrl，那么后续的操作无权限
    postUrl = 'http://www.tianmasport.com/ms/beLogin.do'
    req = requests.post(postUrl, headers=header, cookies=checkCookie, data=form)
    fUrl = 'http://www.tianmasport.com/ms/main.shtml'
    main = requests.get(fUrl, cookies=checkCookie, headers=header)
    info = {
        'cookie':checkCookie,
        'message':req.text
    }
    print(req.text)
    return info


app = Flask(__name__)  # 创建一个服务，赋值给APP

@app.route('/getGoodsInfo', methods=['POST'])  # 指定接口访问路径，支持什么请求方式get,post
def getGoodsInfo():
    # 提交post请求获取商品数据
    byIDUrl = 'http://www.tianmasport.com/ms/order/searchByArticleno.do'
    # .decode('utf-8')
    reqs = request.get_data().decode('utf-8')
    reqss = re.split('&', reqs)
    articleno = reqss[0][7:]
    size = reqss[1][5:]
    articlenoData = {
        'articleno': articleno,
        'size': size
    }

    byID = requests.post(byIDUrl, cookies=info['cookie'], headers=header, data=articlenoData)
    byID.encoding = 'utf-8'
    soup = BeautifulSoup(byID.text, "html.parser")
    '''
    strs = str(soup.find_all("script")[-1])
    pJIndex = strs.index("$.parseJSON")
    pJLast = strs.index("}]}');")
    sizeIndex = strs.index("size_info = '")
    sizeLast = strs.index('.split(",");')
    goodsInfo = json.loads(strs[pJIndex + 13:pJLast + 3])
    goodssize = (re.split(',', strs[sizeIndex + 13:sizeLast - 1]))[0:-1]
    databacks = {}
    i = 1
    for size in goodssize:
        sizestr = re.split('<>', size)
        if articlenoData['size'] == sizestr[1]:
            for info in goodsInfo['rows']:
                if sizestr[2] in info:
                    databack = {
                        'wareHouseName': info['wareHouseName'],
                        sizestr[2]: info[sizestr[2]],
                        'proxyPrice': info['proxyPrice'],
                        'discount': info['discount'],
                        'pickRate': info['pickRate'],
                        'expressName': info['expressName'],
                        'pick_date': info['pick_date']
                    }
                    databacks[str(i)] = databack
                    i += 1
    print(databacks)
    '''
    rsp = make_response(soup.encode('utf-8'))
    rsp.headers['Access-Control-Allow-Origin'] = '*'
    print(rsp)
    return rsp

if __name__ == '__main__':
    info = simLogin()
    while 'false' in info['message']:
        info = simLogin()
    app.run(host=IP, port=port)

