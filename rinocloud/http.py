
import rinocloud
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
from clint.textui.progress import Bar as ProgressBar
from clint.textui import progress
import json


def upload(filepath=None, meta=None):
    encoder = MultipartEncoder(
        fields={
            'file': ('file', open(filepath, 'rb')),
            'json': json.dumps(meta)
        }
    )

    encoder_len = encoder.len
    bar = ProgressBar(expected_size=encoder_len, filled_char='#')

    def callback(monitor):
        bar.show(monitor.bytes_read)

    m = MultipartEncoderMonitor(encoder, callback)

    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': m.content_type
    }

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


def download(_id, filepath, size):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }
    r = requests.get(rinocloud.urls["download"] + str(_id), stream=True, headers=headers)
    with open(filepath, 'wb') as f:
        total_length = size
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    return r


def query(query):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    return requests.post(rinocloud.urls["query"], json={'query': query}, headers=headers)