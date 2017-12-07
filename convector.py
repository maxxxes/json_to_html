import json
from collections import OrderedDict


class JsonLoads:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, json.decoder.JSONDecodeError):
            print('Не правильный формат JSON файла:')
            print(exc_val)
        return True


TAGS_RENDER_DEFAULT = {
    'title': 'h1',
    'body': 'p'
}


def render_el(value, tag):
    return '<{tag}>{value}</{tag}>'.format(value=value, tag=tag)


def render_obj(obj, key_tag=None):
    res = ''
    for (key, val) in obj.items():
        res += render_el(val, key if key_tag else TAGS_RENDER_DEFAULT[key])
    return res


def render_html(source):
    res = ''
    if isinstance(source, list):
        for o in source:
            res += render_obj(o, key_tag=True)
    else:
        res += render_obj(source, key_tag=True)
    print(res)


def main():
    with open('source.json') as json_file, JsonLoads():
        source = json.loads(json_file.read(), object_pairs_hook=OrderedDict)
        render_html(source)

if __name__ == '__main__':
    main()
