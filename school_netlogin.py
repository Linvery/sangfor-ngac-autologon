#-*-coding:utf-8-*-
import requests
import os
import time
import socket
import json

# ping命令


def ping():
    result = os.system(u"ping 114.114.114.114 -n 3")
    return result

# POST包
def Network_Auth():
    url = "http://1.1.1.3/ac_portal/login.php"
    f = open('post.ini')
    data=json.loads(f.read())
    try:
        r = requests.post(url, data)
        # 返回的是HTTP回应包
    except:
        return None
    else:
        login_status = r.text
        return login_status


def log(status, message):
    # 获取本地时间
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #检测log文件夹是否存在
    isExists = os.path.exists('log')
    if not isExists:
        os.makedirs('log')  #如果log文件夹不存在则创建

    # 写入日志到log.txt
    log = open("log/log.txt", 'a+', encoding='utf8')
    if status == 0:
        log.write("Time:{} Status:{} 网络正常\n".format
                   (localtime, status))
    elif status == 1 or 2 or 3:
        log.write("Time:{} Status:{} 响应包状态:{}\n".format
                   (localtime, status, message))
    log.close()


if __name__ == '__main__':
    if ping() == 0:
        print("网络正常！")
        print("当前认证状态：Success")
        status = 0
        #禁用网络正常时写入log，以免产生过大的log文件。
        #log(status, None)  
    else:
        try:
            re_message = Network_Auth()  # 返回的是HTTP回应包
            message = re_message[1:16].split(':')
            if message[1] == 'true,':
                status = 1
                log(status, message)
                print("无法连接到网络！原因：未认证")
                print("尝试认证成功！")
                print("当前认证状态：Success")
            elif message[1] == 'false':
                status = 2
                log(status, message)
                print("无法连接到网络！原因：尝试请求认证，但未成功")
                print("请检查post.ini中的账号和密钥")
                print("当前认证状态：False")
        except:
            status = 3
            message = "None"
            log(status, message)
            print("无法连接到网络！原因：无法连接到认证服务器")
            print("请检查本地网络设置")
            print("当前认证状态：False")