"""
data_generator.py
- generates bunch of needed data for mocking

Created by Xiong Kaijie on 2022-08-15.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from faker import Faker
import random
from datetime import datetime


fake = Faker()


class UserMaterial():

    ip = [fake.ipv4() for _ in range(50)]
    browser = [fake.user_agent() for _ in range(10)]
    tag = ['TagA', 'TagB', 'TagC', 'TagD', 'TagE', 'TagF']
    page = [fake.uri() for _ in range(10)]
    device_os = [
        {
            'device': ['iPhone 11', 'iPhone 12', 'iPhone SE'],
            'os': ['iOS 15.5', 'iOS 13.1', 'iOS 14.3']
        },
        {
            'device': ['MacBook Air', 'MacBook Pro', 'iMac'],
            'os': ['macOS Monterey', 'macOS Big Sur', 'macOS Mojave']
        },
        {
            'device': ['PC', 'Surface',],
            'os': ['Windows 10', 'Windows 11']
        },
        {
            'device': ['Huawei P50', 'Nubia Z17', 'OPPO R11', 'Xiaomi 12S Ultra'],
            'os': ['Android 12.1.2', 'Android 11.0.5']
        }
    ]

    def generate_user_data(self):
        """generate user mock data

        Returns:
            list: a list of user data dict
        """
        user_list = []
        for ip in self.ip:
            user_info = {}
            device_type = random.randint(0, 3)
            user_info['device'] = random.choice(self.device_os[device_type]['device'])
            user_info['os'] = random.choice(self.device_os[device_type]['os'])
            user_info['browser'] = random.choice(self.browser)
            user_info['ip'] = ip
            user_info['tag'] = random.choice(self.tag)
            user_info['page'] = random.choice(self.page)
            user_list.append(user_info.copy())
        return user_list


class RequestMaterial():

    targetURL = [fake.uri() for _ in range(20)]
    statusCode = ['404', '401', '502', '200', '201', '202', '307']
    timestamp = [fake.date_between_dates(date_start=datetime(2022,7,15), date_end=datetime(2022,8,15)) for _ in range(30)]
    eventType = ['load']
    httpDuration = [str(random.randint(1, 20)) for _ in range(10)]
    dnsDuration = [str(random.randint(1, 20)) for _ in range(10)]
    params = 'name=test'
    responseData = {
        'error': '{"error"}',
        'success': '{"success"}'
    }

    def build_basic_request(self, user):
        request_info = {}
        request_info['user'] = user
        request_info['targetURL'] = random.choice(self.targetURL)
        request_info['statusCode'] = random.choice(self.statusCode)
        request_info['timestamp'] = random.choice(self.timestamp)
        request_info['eventType'] = random.choice(self.eventType)
        request_info['httpDuration'] = random.choice(self.httpDuration)
        request_info['dnsDuration'] = random.choice(self.dnsDuration)
        request_info['params'] = self.params

        if request_info['statusCode'].startswith('4'):
            request_info['is_error'] = True
            request_info['responseData'] = self.responseData['error']
        else:
            request_info['is_error'] = False
            request_info['responseData'] = self.responseData['success']
        
        return request_info

    def generate_request_data(self, users):
        """generate request mock data

        Args:
            users (list of dicts/queryset): can be None

        Returns:
            list: list of request data dict
        """
        request_list = []
        if users:
            for user in users:
                request_list.append(self.build_basic_request(user))
        else:
            for _ in range(50):
                user = {}
                request_list.append(self.build_basic_request(user))
        return request_list



class ErrorMaterial():

    category = ['JS', 'Promise', 'Resource', 'BlankScreen']
    originURL = [fake.uri() for _ in range(20)]
    timestamp = [fake.date_between_dates(date_start=datetime(2022,7,15), date_end=datetime(2022,8,15)) for _ in range(30)]
    errorMsg = {
        'jsErrorMsg': [
            'Uncaught SyntaxError: Invalid or unexpected token',
            'Uncaught SyntaxError: Unexpected string',
            'Uncaught ReferenceError: a is not defined',
            'Uncaught ReferenceError: Invalid left-hand side in assignment',
            'Uncaught RangeError: Invalid array length',
            'Uncaught TypeError: 123 is not a function',
            'Uncaught TypeError: Cannot read property "aa" of undefined',
            'Uncaught TypeError: Cannot set property "error" of undefined',
            'Uncaught URIError: URI malformed'
        ],
        'promiseErrorMsg': [
            'TypeError: failed to fetch...',
        ],
        'resourceErrorMsg': [],
        'requestErrorMsg': [],
        'blankscreenError': []
    }
    filename = [fake.file_path(depth=3, category='text') for _ in range(20)]
    position = '23:13'
    stack = 'btnClick (https://origin.test.com/test:23:13)^HTMLInputElement.onclick (https://origin.test.com/test:14:72)'
    selector = 'test'
    tagNmae = 'SCRIPT'
    rsrcTimestamp = '233'
    emptyPoints = '0'
    screen = '2049x1152'
    viewPoint = '2048x994'

    def build_basic_error(self, user):
        error_info = {}
        error_info['user'] = user
        error_info['category'] = random.choice(self.category)
        error_info['originURL'] = random.choice(self.originURL)
        error_info['timestamp'] = random.choice(self.timestamp)

        if error_info['category'] == 'JS':
            error_info['errorType'] = 'jsError'
            error_info['errorMsg'] = random.choice(self.errorMsg['jsErrorMsg'])
            error_info['filename'] = random.choice(self.filename)
            error_info['position'] = self.position
            error_info['stack'] = self.stack
            error_info['selector'] = self.selector

        elif error_info['category'] == 'Promise':
            error_info['errorType'] = 'promiseError'
            error_info['errorMsg'] = random.choice(self.errorMsg['promiseErrorMsg'])
            error_info['filename'] = random.choice(self.filename)
            error_info['position'] = self.position
            error_info['stack'] = self.stack
            error_info['selector'] = self.selector

        elif error_info['category'] == 'Resource':
            error_info['errorType'] = 'resourceError'
            error_info['filename'] = random.choice(self.filename)
            error_info['tagName'] = self.tagNmae
            error_info['rsrcTimestamp'] = self.rsrcTimestamp
            error_info['selector'] = self.selector

        elif error_info['category'] == 'BlankScreen':
            error_info['errorType'] = 'blankscreenError'
            error_info['emptyPoints'] = self.emptyPoints
            error_info['screen'] = self.screen
            error_info['viewPoint'] = self.viewPoint
            error_info['selector'] = self.selector
        
        return error_info

    def generate_error_data(self, users):
        """generate error mock data

        Args:
            users (list of dicts/queryset): can be None

        Returns:
            list: list of error data dict
        """
        error_list = []
        if users:
            for user in users:
                error_list.append(self.build_basic_error(user))
        else:
            for _ in range(100):
                user = {}
                error_list.append(self.build_basic_error(user))
                
        return error_list

