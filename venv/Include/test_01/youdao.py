import requests
import json


def get_translate_date(word=None):
    url = 'http://fanyi.youdao.com/translate'
    # url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    Form_data = {'i': word,
                 'from': 'AUTO',
                 'to': 'AUTO',
                 'smartresult': 'dict',
                 'client': 'fanyideskweb',
                 'salt': '15743412838440',
                 'sign': '0774a3f8108f6bfcd9135646fcdea51a',
                 'ts': '1574341283844',
                 'bv': '75551116684a442e8625ebfc9e5af1ba',
                 'doctype': 'json',
                 'version': '2.1',
                 'keyfrom': 'fanyi.web',
                 'action': 'FY_BY_REALTlME'}
    response = requests.post(url, data=Form_data)
    content = json.loads(response.text)
    print(content['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    get_translate_date('我爱翻译')
