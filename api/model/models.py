"""
models.py
- for defining classes that will serve as data objects for the server

Created by Xiong Kaijie on 2022-08-01.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from flask_mongoengine import MongoEngine
from mongoengine import *
from datetime import datetime

db = MongoEngine()


class UserExample(Document):
    """用户数据结构

    用户 ID: _id
    设备 (device)
    操作系统 (os)
    浏览器 (browser)
    网络制式 (network)
    IP (ip)
    """

    device = StringField()
    os = StringField()
    browser = StringField()
    network = StringField()
    ip = StringField()

    meta = {
        'collection': 'user',
        'ordering': ['-id']
    }


class RequestExample(Document):
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

    user = ReferenceField(UserExample)
    targetURL = StringField(required=True)
    statusCode = StringField(required=True)
    timestamp = DateTimeField(required=True)
    eventType = StringField()
    httpDuration = StringField()
    dnsDuration = StringField()
    params = StringField()
    responseData = StringField()
    is_error = BooleanField(required=True, default=False)

    meta = {
        'collection': 'requestData',
        'ordering': ['-timestamp']
    }


class ErrorExample(DynamicDocument):
    """
    """

    category = StringField(required=True)
    originURL = StringField(required=True)
    timestamp = DateTimeField(required=True, default=datetime.utcnow)
    user = ReferenceField(UserExample)
    requestData = ReferenceField(RequestExample)
    errorType = StringField()
    errorMsg = StringField()
    filename = StringField()
    position = StringField()
    stack = StringField()
    selector = StringField()
    tagName = StringField()
    rsrcTimestamp = StringField()
    emptyPoints = StringField()
    screen = StringField()
    viewPoint = StringField()

    meta = {
        'collection': 'errorData',
        'ordering': ['-timestamp'],
    }
