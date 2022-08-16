"""
models.py
- for defining classes that will serve as data objects for the server

Created by Xiong Kaijie on 2022-08-01.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from flask_mongoengine import MongoEngine
# from mongoengine import *
from datetime import datetime
import bson.json_util as json_util
import json
from ...util.utils import convert_utc_to_local

db = MongoEngine()


# class UserExample(Document):
#     """用户数据结构

#     用户 ID: _id
#     设备 (device)
#     操作系统 (os)
#     浏览器 (browser)
#     网络制式 (network)
#     IP (ip)
#     """

#     device = StringField()
#     os = StringField()
#     browser = StringField()
#     network = StringField()
#     ip = StringField()

#     meta = {
#         'collection': 'user',
#         'ordering': ['-id']
#     }


# class RequestExample(Document):
#     """请求数据结构

#     请求 ID (requestID): _id
#     用户 ID (userID {用户}['_id'])
#     请求目标 URL 地址 (targetURL)
#     状态码 (statusCode)
#     时间戳 (timestamp 请求触发时间)
#     事件类型 (eventType load/error/abort)
#     HTTP持续时间 (httpDuration)
#     DNS持续时间 (dnsDuration)
#     请求参数 (params URL Body/URL Parameters)
#     响应内容 (responseData return value)
#     """

#     user = ReferenceField(UserExample)
#     targetURL = StringField(required=True)
#     statusCode = StringField(required=True)
#     timestamp = DateTimeField(required=True)
#     eventType = StringField()
#     httpDuration = StringField()
#     dnsDuration = StringField()
#     params = StringField()
#     responseData = StringField()
#     is_error = BooleanField(required=True, default=False)

#     meta = {
#         'collection': 'requestData',
#         'ordering': ['-timestamp']
#     }


# class ErrorExample(DynamicDocument):
#     """
#     """

#     category = StringField(required=True)
#     originURL = StringField(required=True)
#     timestamp = DateTimeField(required=True, default=datetime.utcnow)
#     user = ReferenceField(UserExample)
#     requestData = ReferenceField(RequestExample)
#     errorType = StringField()
#     errorMsg = StringField()
#     filename = StringField()
#     position = StringField()
#     stack = StringField()
#     selector = StringField()
#     tagName = StringField()
#     rsrcTimestamp = StringField()
#     emptyPoints = StringField()
#     screen = StringField()
#     viewPoint = StringField()

#     meta = {
#         'collection': 'errorData',
#         'ordering': ['-timestamp'],
#     }


class User(db.DynamicDocument):
    """用户数据结构

    用户 ID: _id
    设备 (device)
    操作系统 (os)
    浏览器 (browser)
    网络制式 (network)
    IP (ip)
    地区 (location)

    """

    device = db.StringField()
    os = db.StringField()
    browser = db.StringField()
    ip = db.StringField()
    tag = db.StringField()
    page = db.StringField()

    meta ={
      'collection':'user',
      'ordering':['-id']
    }

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def to_dict(self):
        return dict(
            userID = json.loads(json_util.dumps(self.id)),
            device = self.device,
            os = self.os,
            browser = self.browser,
            ip = self.ip,
            tag = self.tag,
            page = self.page
        )


class RequestData(db.DynamicDocument):
    """请求数据结构
    
    请求 ID (requestID): _id
    用户 ID (userID {用户}['_id'])
    请求目标 URL 地址 (targetURL)
    状态码 (statusCode)
    时间戳 (timestamp 请求触发时间)
    事件类型 (eventType load/error/abort)
    HTTP持续时间 (httpDuration)
    DNS持续时间 (dnsDuration)
    请求参数 (params URL Body/URL Parameters)
    响应内容 (responseData return value)
    """

    user = db.ReferenceField(User)
    targetURL = db.StringField(required=True)
    statusCode = db.StringField(required=True)
    timestamp = db.DateTimeField(required=True)
    eventType = db.StringField()
    httpDuration = db.StringField()
    dnsDuration = db.StringField()
    params = db.StringField()
    responseData = db.StringField()
    is_error = db.BooleanField(required=True, default=False)

    meta ={
      'collection':'requestData',
      'ordering':['-timestamp']
    }

    def __init__(self, **kwargs):
        super(RequestData, self).__init__(**kwargs)

    def to_dict(self):
        return dict(
            requestID = json.loads(json_util.dumps(self.id)),
            user = self.user.to_dict(),
            targetURL = self.targetURL,
            statusCode = self.statusCode,
            timestamp = convert_utc_to_local(self.timestamp),
            eventType = self.eventType,
            httpDuration = self.httpDuration,
            dnsDuration = self.dnsDuration,
            params = self.params,
            responseData = self.responseData,
            is_error = self.is_error
        )


class ErrorData(db.DynamicDocument):
    """Error data structure
    Requirements:「异常监控, 包括: JS异常、接口异常、白屏异常、资源异常等」

    [基本信息]
        错误 ID: _id
        错误分类 (category JS/Promise/Request/Resource/BlankScreen)
        错误来源 URL 地址 (originURL)
        时间戳 (timestamp 错误的产生时间)

        用户
        请求
        
        {用户}
            用户 ID (触发该错误的当前用户): _id
            设备 (device)
            操作系统 (os)
            浏览器 (browser)
            网络制式 (network)
            IP (ip)
            地区 (location)
        
        #JS异常 JS执行异常
        if categroy == 'JS'
            错误类型 (errorType): 'jsError'
            报错信息 (errorMsg): event.message
            报错文件名 (filename 报错链接): event.filename
            行列号 (position): (event.lineNo || 0) + ":" + (event.columnNo || 0)
            堆栈信息 (stack 包含源文件, 报错位置等): event.error.stack
            选择器信息 (selector CSS选择器): getLastEvent()? getSelector(getLastEvent().path || getLastEvent().target): ""
        
        #JS异常 Promise异常
        if categroy == 'Promise'
            错误类型 (errorType): 'promiseError'
            报错信息 (errorMsg): event.reason || event.reason.message
            报错文件名 (filename): event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[1]
            行列号 (position): event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[2] + ':' + event.reason.stack.match(/at\s+(.+):(\d+):(\d+)/)[3]
            堆栈信息 (stack 包含源文件, 报错位置等): getLines(event.reason.stack)
            选择器信息 (selector CSS选择器): getLastEvent()? getSelector(getLastEvent().path || getLastEvent().target): ""
        
        #资源异常
        if categroy == 'Resource'
            错误类型 (errorType): 'resourceError'
            报错文件名 (filename 加载失败的文件位置): event.target.src || event.target.href
            标签名 (tagName): event.target.tagName
            时间 (rsrcTimestamp): formatTime(event.timeStamp)
            选择器信息 (selector CSS选择器): getSelector(event.path || event.target)

        #接口异常
        if categroy == 'Request'
            错误类型 (errorType): 'requestError'
            {请求} > 如果Request监控出现异常, 则向error表里面添加此request
                请求 ID (requestID): _id
                用户 ID (userID {用户}['_id'])
                请求目标 URL 地址 (targetURL)
                状态码 (statusCode)
                时间戳 (timestamp 请求触发时间)
                事件类型 (eventType load/error/abort)
                HTTP持续时间 (httpDuration)
                DNS持续时间 (dnsDuration)
                请求参数 (params URL Body/URL Parameters)
                响应内容 (response return value)
        
        #白屏异常
        if categroy == 'BlankScreen'
            错误类型 (errorType): 'blankscreenError'
            空白点 (emptyPoints)
            分辨率 (screen)
            视口 (viewPoint)
            选择器 (selector)

    [用户行为回溯信息]
        行为名称
        行为对应项目
        行为时间戳

    [数据统计概况]
        发生总次数
        影响用户数
        发生数时间维度统计

    deviceName = db.StringField()
    deviceOS = db.StringField()
    deviceBrowser = db.StringField()
    ip = db.StringField(required=True, max_length=128)
    """

    category = db.StringField(required=True)
    originURL = db.StringField(required=True)
    timestamp = db.DateTimeField(required=True, default=datetime.utcnow)
    user = db.ReferenceField(User)
    requestData = db.ReferenceField(RequestData)
    errorType = db.StringField()
    errorMsg = db.StringField()
    filename = db.StringField()
    position = db.StringField()
    stack = db.StringField()
    selector = db.StringField()
    tagName = db.StringField()
    rsrcTimestamp = db.StringField()
    emptyPoints = db.StringField()
    screen = db.StringField()
    viewPoint = db.StringField()

    meta = {
        'collection': 'errorData',
        'ordering': ['-timestamp'],
        'allow_inheritance': True,
    }

    def __init__(self, **kwargs):
        super(ErrorData, self).__init__(**kwargs)

    
    def to_dict(self, withUserInfo):
        if self.category == 'JS' or self.category == 'Promise':
            result = {
                    'errorID': json.loads(json_util.dumps(self.id)),
                    'category': self.category,
                    'originURL': self.originURL,
                    'timestamp': convert_utc_to_local(self.timestamp),
                    'errorType': self.errorType,
                    'errorMsg': self.errorMsg,
                    'filename': self.filename,
                    'position': self.position,
                    'stack': self.stack,
                    'selector': self.selector
                }
            if withUserInfo:
                result['user'] = self.user.to_dict()
        elif self.category == 'Resource':
            result = {
                'errorID': json.loads(json_util.dumps(self.id)),
                'category': self.category,
                'originURL': self.originURL,
                'timestamp': convert_utc_to_local(self.timestamp),
                'errorType': self.errorType,
                'filename': self.filename,
                'tagName': self.tagName,
                'rsrcTimestamp': self.rsrcTimestamp,
                'selector': self.selector
            }
            if withUserInfo:
                result['user'] = self.user.to_dict()
        elif self.category == 'Request':
            result = {
                'errorID': json.loads(json_util.dumps(self.id)),
                'category': self.category,
                'originURL': self.originURL,
                'timestamp': convert_utc_to_local(self.timestamp),
                'errorType': self.errorType,
                'requestData': self.requestData.to_dict()
            }
            # if withUserInfo:
            #     result['user'] = self.user.to_dict()
        elif self.category == 'BlankScreen':
            result = {
                'errorID': json.loads(json_util.dumps(self.id)),
                'category': self.category,
                'originURL': self.originURL,
                'timestamp': convert_utc_to_local(self.timestamp),
                'errorType': self.errorType,
                'emptyPoints': self.emptyPoints,
                'screen': self.screen,
                'viewPoint': self.viewPoint,
                'selector': self.selector
            }
            if withUserInfo:
                result['user'] = self.user.to_dict()
        return result