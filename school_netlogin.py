#-*-coding:utf-8-*-
import requests
import os
import time
import json
import platform
import rc4

# ping命令
def ping():
    #判断操作系统
    sys = platform.system()
    if sys == "Windows":
        result = os.system(u"ping 114.114.114.114 -n 1")
    elif sys == "Linux":
        result = os.system(u"ping 114.114.114.114 -c 3")
    return result

# POST包
def Network_Auth():
    url = "http://1.1.1.3/ac_portal/login.php"
    
    #构建POST包
    #js加密方式：userName=明文;pwd=rc4加密(rc4Key,用户密码);rc4Key=当前时间13位时间戳
    data={
    "opr": "pwdLogin",
    "userName": "",
    "pwd": "",
    "rc4Key": "",
    "rememberPwd": "1"
    }
    f = open('profile.ini') #读配置文件
    f1=f.read()

    f1=json.loads(f1)   #用json方法字符串转字典
    profile_passwd=f1["password"]   #用户名

    now_date = str(int(round(time.time()*1000)))    #获取当前时间
    secert_pass=rc4.encrypt(now_date,profile_passwd)    #rc4加密

    #写回到data字典中
    data['userName']=f1["username"]
    data['pwd']=secert_pass
    data['rc4Key']=now_date
    #print(data)

    try:
        r = requests.post(url, data)
    except:
        return None
    else:
        login_status = r.text   # 返回的是HTTP响应包
        return login_status


def log(status, message):
    # 获取本地时间
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    #检测log文件夹是否存在
    isExists = os.path.exists('log')
    if not isExists:
        os.makedirs('log')  #如果log文件夹不存在则创建

    # 写入日志到log.txt
    log = open("log/log.txt", 'a+')
    if code == 0:
        log.write("Time:{} Code:{} Online!\n".format
                   (localtime, code))
    elif code == 1 or 2 or 3:
        log.write("Time:{} Code:{} Response:{}\n".format
                   (localtime, code, message))
    log.close()


if __name__ == '__main__':
    if ping() == 0:
        print("网络正常！")
        print("当前认证状态：Success")
        code = 0
        #禁用网络正常时写入log，以免产生过大的log文件。
        #log(status, None)  
    else:
        try:
            re_message = Network_Auth()  # 返回的是HTTP回应包
            message = re_message[1:16].split(':')
            message[0]=message[0].replace("'","")  
            # print(re_message)
            # print(message)
            if message[1] == 'true,':
                code = 1
                message[1]=message[1].replace(",","")
                log(code, message)
                print("无法连接到网络！原因：未认证")
                print("尝试认证成功！")
                print("当前认证状态：Success")
            elif message[1] == 'false':
                code = 2
                log(code, message)
                print("无法连接到网络！原因：尝试请求认证，但未成功")
                print("请检查post.ini中的账号和密钥")
                print("当前认证状态：False")
        except:
            code = 3
            message = "None"
            log(code, message)
            print("无法连接到网络！原因：无法连接到认证服务器或配置错误")
            print("请检查本地网络设置")
            print("当前认证状态：False")