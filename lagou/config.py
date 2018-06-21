#!/usr/bin/python 
# -*- coding: utf-8 -*- 
import os

try:
    path = os.getcwd()+'/user.json'
    file = open(path, 'r')
    info = eval(file.read())
except Exception as e:
    print(os.getcwd(),'/user.json获取失败')
    raise 

lagou_user = info['lagou_user']
lagou_psw   = info['lagou_psw']
email_user = info['email_user']
email_auth_psw = info['email_auth_psw']
email_receiver = info['email_receiver']