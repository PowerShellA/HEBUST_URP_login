import requests
import base64
import hashlib
import time
import urllib
import os
import pytesseract
from PIL import Image
import json
#from flask import Flask,jsonify
#from bs4 import BeautifulSoup


def scan_jpg(filename):
    image = Image.open(filename)
    image = image.convert('L')
    threshold = 119
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    result = pytesseract.image_to_string(image,config='digits').replace(" ","")
    print(result)
    return result


def get_code():
    now_time = time.strftime("%a %b %d %Y %H:%M:%S", time.localtime()) + " GMT 0800"
    jpg_url = "http://202.206.64.206/hbkjjw/cas/genValidateCode?dateTime=" + urllib.parse.quote(now_time)
    jpg = urllib.request.urlopen(jpg_url)
    pic_data = jpg.read()
    localtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
    filename = localtime + ".jpg"
    f = open(filename, "wb")
    f.write(pic_data)
    f.close()
    jessionid = jpg.headers._headers[2][1][11:-8]
    #print(jessionid)
    try:
        code = str(scan_jpg(filename))
        os.remove(filename)
        if code.isdigit() and len(code) == 4 and code is not None:
            codea = code
            jessionid = jessionid
            return codea, jessionid
        else:
            codea = get_code()
    except:
        os.remove(filename)
        codea = get_code()
    return codea


def hex_md5(data):
    return hashlib.md5(data.encode(encoding='UTF-8')).hexdigest()


def login(username,password):
    global randnumber
    global jessionid
    global header
    global params
    temp = get_code()
    randnumber = temp[0]
    jessionid = temp[1]
    # print(temp)
    txt_mm_expression = "11"  # get_mm_expression(password)
    txt_mm_length = str(len(password))
    txt_mm_userzh = "0"  # str(len(username))
    password = str(hex_md5(hex_md5(password) + hex_md5(randnumber)))
    p_username = "_u" + randnumber
    p_password = "_p" + randnumber
    username_to_encrypt = username + ";;" + jessionid
    username = str(base64.b64encode(username_to_encrypt.encode('utf-8')))[2:-1]
    params = {
        p_username: username,
        p_password: password,
        'randnumber': randnumber,
        'isPasswordPolicy': "1",
        'txt_mm_expression': txt_mm_expression,
        'txt_mm_length': txt_mm_length,
        'txt_mm_userzh': txt_mm_userzh
    }
    header = {
        "Cookie": "JSESSIONID=" + jessionid,
        "Origin": "http://202.206.64.206",
        "Accept-Encoding": "gzip, deflate",
        "Host": "202.206.64.206",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/plain, */*; q=0.01",
        "Referer": "http://202.206.64.206/hbkjjw/cas/login.action",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Content-Length": "196",
        "DNT": "1"
    }
    login_res = requests.post("http://202.206.64.206/hbkjjw/cas/logon.action", headers=header, data=params)

def logout(jessionid):
    header_out = {
        "Cookie": "JSESSIONID=" + jessionid,
        "Origin": "http://202.206.64.206",
        "Accept-Encoding": "gzip, deflate",
        "Host": "202.206.64.206",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/plain, */*; q=0.01",
        "Referer": "http://202.206.64.206/hbkjjw/frame/Main_tools.jsp",
        "Upgrade - Insecure - Requests": "1",
        "Connection": "keep-alive",
        "DNT": "1"
    }
    logout_res = requests.get("http://202.206.64.206/hbkjjw/DoLogoutServlet", headers = header_out)


jessionid = ""
randnumber = ""
header = {}
params = {}

temp = get_code()
print(temp)


#login("170705111","xxxxxxxxxxxx")
#logout(jessionid)