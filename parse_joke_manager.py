import urllib3
import orjson


def get_new_joke():
    http = urllib3.PoolManager()
    encoded_data = orjson.dumps({"content": "value"})
    resp = http.request(method="POST", url="http://rzhunemogu.ru/RandJSON.aspx?CType=1", body=encoded_data,
                           decode_content=True)
    raw_data = resp.data.decode("windows-1251")
    begin_joke_text_index = 12
    end_joke_text_index = -2
    joke = raw_data[begin_joke_text_index: end_joke_text_index]
    return joke
