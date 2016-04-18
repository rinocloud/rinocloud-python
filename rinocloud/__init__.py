# Rinocloud Python bindings
# API docs at http://github.com/rinocloud/rinocloud-python
# Authors:
# Jamie Lee <jamie@rinocloud.com>
# Eoin Murray <eoin@rinocloud.com>

api_key = None
api_base = 'http://staging.rinocloud.com/api/1/'
# api_base = 'http://localhost:8000/api/1/'

from object import Object
import http as http

urls = {
    'upload': api_base + 'files/upload_multipart/',
    'get': api_base + 'files/get_metadata/',
    'update': api_base + 'files/update_metadata/',
    'download': api_base + 'files/download/?id=',
    'query': api_base + 'files/query/',
    'sign_s3': api_base + 'files/sign_s3/',
    'pre_s3_upload': api_base + 'files/pre_s3_upload/',
    'post_s3_upload': api_base + 'files/post_s3_upload/',
}
