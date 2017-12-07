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
    if isinstance(value, list):
        value = render_objects(value)
    return '<{tag}>{value}</{tag}>'.format(value=value, tag=tag)


def render_li_decorator(func):
    def func_wrapper(*args, **kwargs):
        return '<li>' + func(*args, **kwargs) + '</li>'
    return func_wrapper


def render_ul_decorator(func):
    def func_wrapper(*args, **kwargs):
        return '<ul>' + func(*args, **kwargs) + '</ul>'
    return func_wrapper


def render_obj(obj, key_tag=None):
    return ''.join(
        render_el(val, key if key_tag else TAGS_RENDER_DEFAULT[key])
        for (key, val) in obj.items()
    )


@render_ul_decorator
def render_objects(source):
    return ''.join(
        render_li_decorator(render_obj)(obj, key_tag=True)
        for obj in source
    )


def render_html(source):
    if isinstance(source, list):
        return render_objects(source)
    return render_obj(source, key_tag=True)


def main():
    with open('source.json') as json_file, JsonLoads():
        source = json.loads(json_file.read(), object_pairs_hook=OrderedDict)
        print(render_html(source))


if __name__ == '__main__':
    main()
