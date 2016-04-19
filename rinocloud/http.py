
import rinocloud
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from clint.textui.progress import Bar as ProgressBar
import json


def create_callback(encoder):
    encoder_len = encoder.len
    bar = ProgressBar(expected_size=encoder_len, filled_char='#')

    def callback(monitor):
        bar.show(monitor.bytes_read)

    return callback


def upload(filepath=None, meta=None):
    encoder = MultipartEncoder(
        fields={
            'file': ('file', open(filepath, 'rb')),
            'json': json.dumps(meta)
        }
    )

    callback = create_callback(encoder)
    m = MultipartEncoderMonitor(encoder, callback)
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': m.content_type
    }

    # this is how you pass files to requests
    # file = {'file': open(filepath, 'rb')}
    # the ugly way we pass the data is a limitation of the upload_multipart api endpoint
    # data = {'json': json.dumps(meta)}

    return requests.post(rinocloud.urls["upload"], data=m, headers=headers)


def upload_meta(meta):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.post(rinocloud.urls["upload_meta"], json=meta, headers=headers)


def get_metadata(_id):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.post(rinocloud.urls["get_metadata"], json={'id': _id}, headers=headers)


def download(_id):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.get(rinocloud.urls["download"] + str(_id), stream=True, headers=headers)


def query(query):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.post(rinocloud.urls["query"], json={'query': query}, headers=headers)
