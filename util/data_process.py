"""
data_process.py
- for data processing

Created by Xiong Kaijie on 2022-08-15.
Contributed by: Xiong Kaijie
Copyright © 2022 team Root of ByteDance Youth Camp. All rights reserved.
"""

from ..api.model.models import User, RequestData, ErrorData


def merge_failed_request(origin_url):
    errorReqs = RequestData.objects(is_error=True)

    if errorReqs:
        for errorReq in errorReqs:
            error_info = {}
            error_info['category'] = 'Request'
            error_info['errorType'] = 'requestError'
            error_info['originURL'] = origin_url if origin_url else 'test.com/test'
            error_info['timestamp'] = errorReq['timestamp']
            error_info['requestData'] = errorReq
            new_error = ErrorData(**error_info)
            new_error.save()


def get_error_overview():
    print('test')

