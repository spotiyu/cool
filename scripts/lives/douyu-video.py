# 获取斗鱼直播间的真实流媒体地址，默认最高画质
# https://github.com/SeaHOH/ykdl/blob/2242de9e0017b383c846661a8c9baf2dd0e8209f/ykdl/extractors/douyu/video.py
import hashlib
import re
import time
# import json
import uuid
import execjs
import requests

from scripts.base import Base

class DouYuVideo(Base):

    _name = 'DOUYU_VIDEO'

    def __init__(self, rid):
        super(Base, self).__init__()
        self.rid = rid

    @staticmethod
    def md5(data):
        return hashlib.md5(data.encode('utf-8')).hexdigest()

    def get_real_url(self):
    
        self.s = requests.Session()
        
        # urlb = 'https://pb.milso.ml/view/raw/3a2c665b'
        # urlc = 'https://pb.milso.ml/view/raw/46883afc'
        # self.did = self.s.get(urlb).text
        # acf_auth = self.s.get(urlc).text
        
        self.did = uuid.uuid4().hex
        self.did = '5adb1572394c2d21fc89e26700021601'
        
        self.t10 = str(int(time.time()))
        # self.t13 = str(int((time.time() * 1000)))
    
        vurl = 'https://v.douyu.com/show/' + self.rid
        self.res1 = self.s.get(vurl).text
        # point_id":24478542,
        result1 = re.search(r'point_id":(\d{1,13}),"cid1', self.res1)
        if result1:
            self.pid = result1.group(1)
        else:
            return '视频地址错误'
        
        result = re.search(r'(var vdwdae325w_64we =[\s\S]+?)\s*<\/script>', self.res1).group(1)
        
        func_ub9 = re.sub(r'eval.*?;}', 'strc;}', result)
        js_ub9 = execjs.compile(func_ub9)
        res_ub9 = js_ub9.call('ub98484234')
        
        v = re.search(r'v=(\d+)', res_ub9).group(1)
        rb = DouYuVideo.md5(self.pid + self.did + self.t10 + v)
        
        func_sign = re.sub(r'return rt;}\);*', 'return rt;}', res_ub9)
        func_sign = func_sign.replace('(function (', 'function sign(')
        func_sign = func_sign.replace('CryptoJS.MD5(cb).toString()', '"' + rb + '"')
        
        js_sign = execjs.compile(func_sign)
        params = js_sign.call('sign', self.pid, self.did, self.t10)
        
        data = params + '&vid=' + self.rid
        
        url = 'https://v.douyu.com/api/stream/getStreamUrl'
        
        headers = {'Content-Type': 'application/x-www-form-urlencoded','Referrer': vurl}
        res = self.s.post(url, headers=headers, data=data).text
        # cookies = {'dy_did': self.did, 'acf_auth': acf_auth}
        # res = self.s.post(url, data=data, headers=headers, cookies=cookies).json()
        
        return res

if __name__ == '__main__':
    r = input('输入斗鱼视频链接：\n')
    s = DouYuVideo(r)
    print(s.get_real_url())
