import base64
import requests

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA

from test_runner import models


class GetToken():
    def __init__(self, project, publickeyurl, loginurl, username, password):
        self.project = project
        self.publickeyurl = publickeyurl
        self.loginurl = loginurl
        self.username = username
        self.password = password

    def login_gettoken(self):
        header = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        data = {
            "userid": self.encrpt(self.username),
            "password": self.encrpt(self.password),
            "client": "webApp",
            "codeId": "",
            "code": ""
        }
        logintoken = requests.post(self.loginurl, json=data, headers=header).json()['data']['access_token']
        variable = models.Variable.objects.filter(project__id=self.project, key="access_token").first()
        if variable:
            variable.value = logintoken
            variable.save()
        else:
            data = {
                "key": "access_token",
                "value": logintoken,
                "project": models.Project.objects.get(id=self.project)
            }
            models.Variable.objects.create(**data)

    def get_public_key(self):
        "获取公钥"
        key = requests.get(self.publickeyurl).json()['data']
        public_key = '-----BEGIN PUBLIC KEY-----\n' + key + '\n-----END PUBLIC KEY-----'
        return public_key

    def encrpt(self, key):
        public_key = self.get_public_key()
        rsakey = RSA.importKey(public_key)
        # 生成对象
        cipher = PKCS1_v1_5.new(rsakey)
        # 对传递进来的用户名或密码字符串加密
        cipher_text = base64.b64encode(cipher.encrypt(key.encode(encoding="utf-8")))
        # 将加密获取到的bytes类型密文解码成str类型
        value = cipher_text.decode('utf8')
        return value