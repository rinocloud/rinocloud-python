
import rinocloud
import requests
import json


def upload(filepath, meta):
    headers = {
        'Authorization': 'Token %s' % rinocloud.api_key,
        'X-Requested-With': 'XMLHttpRequest'
    }

    file = {'file': open(filepath, 'rb')}
    data = {'json': json.dumps(meta)}

    return requests.post(rinocloud.urls["upload"], files=file, data=data, headers=headers)
