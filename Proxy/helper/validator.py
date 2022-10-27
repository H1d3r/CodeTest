# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     _validators
   Description :   定义proxy验证方法
   Author :        JHao
   date：          2021/5/25
-------------------------------------------------
   Change Activity:
                   2021/5/25:
-------------------------------------------------
"""
__author__ = 'JHao'

from re import findall
from requests import head,get
from Proxy.util.six import withMetaclass
from Proxy.util.singleton import Singleton
from Proxy.handler.configHandler import ConfigHandler

conf = ConfigHandler()

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
          'Accept': '*/*',
          'Connection': 'keep-alive',
          'Accept-Language': 'zh-CN,zh;q=0.8'}


class ProxyValidator(withMetaclass(Singleton)):
    pre_validator = []
    http_validator = []
    https_validator = []
    anonymous_validator = []
    socks5_validator = []
    socks4_validator = []

    @classmethod
    def addPreValidator(cls, func):
        cls.pre_validator.append(func)
        return func

    @classmethod
    def addHttpValidator(cls, func):
        cls.http_validator.append(func)
        return func

    @classmethod
    def addHttpsValidator(cls, func):
        cls.https_validator.append(func)
        return func
    
    @classmethod
    def addSocks5Validator(cls, func):
        cls.socks5_validator.append(func)
        return func
    
    @classmethod
    def addSocks4Validator(cls, func):
        cls.socks4_validator.append(func)
        return func

    @classmethod
    def addAnonymousValidator(cls, func):
        cls.anonymous_validator.append(func)
        return func


@ProxyValidator.addPreValidator
def formatValidator(proxy):
    """检查代理格式"""
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = findall(verify_regex, proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy else False


@ProxyValidator.addHttpValidator
def httpTimeOutValidator(proxy):
    """ http检测超时 """

    proxies = {"http": "http://{proxy}".format(proxy=proxy.proxy), "https": "https://{proxy}".format(proxy=proxy.proxy)}
    try:
        r = head(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #r = get(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout)
        #return True if r.status_code == 200 and ',' not in r.text else False
        return True if r.status_code == 200 else False
    except Exception as e:
        return False


@ProxyValidator.addHttpsValidator
def httpsTimeOutValidator(proxy):
    """https检测超时"""

    proxies = {"http": "http://{proxy}".format(proxy=proxy.proxy), "https": "https://{proxy}".format(proxy=proxy.proxy)}
    try:
        r = head(conf.httpsUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #r = get(conf.httpsUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #return True if r.status_code == 200 and ',' not in r.text else False
        return True if r.status_code == 200 else False
    except Exception as e:
        return False

@ProxyValidator.addSocks5Validator
def socks5TimeOutValidator(proxy):
    """socks5检测超时"""

    proxy = 'socks5://{}'.format(proxy.proxy)
    proxies = {"http": proxy, "https": proxy}
    try:
        r = head(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #r = get(conf.httpsUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #return True if r.status_code == 200 and ',' not in r.text else False
        return True if r.status_code == 200 else False
    except Exception as e:
        return False

@ProxyValidator.addSocks4Validator
def socks4TimeOutValidator(proxy):
    """socks4检测超时"""

    proxy = 'socks4://{}'.format(proxy.proxy)
    proxies = {"http": proxy, "https": proxy}
    try:
        r = head(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #r = get(conf.httpsUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        #return True if r.status_code == 200 and ',' not in r.text else False
        return True if r.status_code == 200 else False
    except Exception as e:
        return False

@ProxyValidator.addAnonymousValidator
def customValidatorExample(proxy):
    """自定义validator函数，校验代理是否可用, 返回True/False"""
    """高匿代理检测"""
    proxies = {"http": "http://{proxy}".format(proxy=proxy.proxy), "https": "https://{proxy}".format(proxy=proxy.proxy)}
    try:
        r = get(conf.httpUrl, headers=HEADER, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        return True if r.status_code == 200 and ',' not in r.text else False
        #return True if r.status_code == 200 else False
    except Exception as e:
        return False
    #return True
