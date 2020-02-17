import  jwt

import datetime

password = 'ida89das8d9a98'

#payload = {'name':'tom','ts':int(datetime.datetime.now().timestamp())}
payload = {'name':'tom','age':20}
pwd = jwt.encode(payload,password,'HS256')
print(pwd)
# b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoidG9tIiwidHMiOjE1ODE4NjcwMTN9.9BpaZKwb4BGioAmfaTXIIP5-EzugFkqtUR6oTobgJ7s'

import base64

def fix(src):
    rem = len(src) % 4
    return src + b'=' * rem




header,pld,sig = pwd.split(b'.')
print(header)
print(pld)
print(sig)

print(base64.urlsafe_b64decode(header))
print(base64.urlsafe_b64decode(fix(pld)))
print(base64.urlsafe_b64decode(fix(sig)))


from jwt.algorithms import  get_default_algorithms
al_obj = get_default_algorithms()['HS256']
print(al_obj)
newkey = al_obj.prepare_key(password) # key 预处理
print(newkey)


sig_input,_,_ = pwd.rpartition(b'.')  #
print(sig_input)


crypt = al_obj.sign(sig_input,newkey)
print(crypt)

print(sig)
print(base64.urlsafe_b64encode(crypt))
# header ，有数据类型，加密算法构成
# payload ，负载就是要传输的数据，一般来说放入python 对象即可，会被json 序列化的
# signature，签名的部分，是前面2部分数据分别base64 编码生使用点号连接后，加密算法使用key 计算好一个结果，再被base64 编码而得到的签名
#