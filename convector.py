import json
import html
import re
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


def render_value_tag(value, safe=None):
    """ Обработка значения тега с защитой от лишних тегов """
    if safe:
        return html.escape(value)
    return value


def render_tag(value, tag, safe=None):
    """ Обработка одного тега с id и class """
    re_tag_name = re.compile(r'^(\w+)\.?')
    re_tag_class_list = re.compile(r'\.(\w+[-]\w+)')
    re_tag_id = re.compile(r'#(\w+[-]\w+)')

    tag_name = next(iter(re_tag_name.findall(tag)), None)
    tag_id = next(iter(re_tag_id.findall(tag)), None)
    tag_class_list = ' '.join(cls for cls in re_tag_class_list.findall(tag))
    style_list = (
        tag_name,
        'id="%s"' % tag_id if tag_id else '',
        'class="%s"' % tag_class_list if tag_class_list else ''
    )
    tag_style = ' '.join((s for s in style_list if s))
    return '<{tag_style}>{value}</{tag_name}>'.format(
        tag_style=tag_style,
        value=render_value_tag(value, safe=safe),
        tag_name=tag_name
    )


def render_el(value, tag):
    """ Обработка одного элемента из source """
    safe = None
    if isinstance(value, list):
        value = render_objects(value)
    else:
        safe = True
    return render_tag(value, tag, safe=safe)


def render_li_decorator(func):
    """ Деторатор для элементов списка - li """
    def func_wrapper(*args, **kwargs):
        return '<li>' + func(*args, **kwargs) + '</li>'
    return func_wrapper


def render_ul_decorator(func):
    """ Деторатор для списка - ul """
    def func_wrapper(*args, **kwargs):
        return '<ul>' + func(*args, **kwargs) + '</ul>'
    return func_wrapper


def render_obj(obj, key_tag=None):
    """ Обработка одного объекта из source """
    return ''.join(
        render_el(val, key if key_tag else TAGS_RENDER_DEFAULT[key])
        for (key, val) in obj.items()
    )


@render_ul_decorator
def render_objects(source):
    """ Обработка списка объектов из source в обертке ul-li """
    return ''.join(
        render_li_decorator(render_obj)(obj, key_tag=True)
        for obj in source
    )


def render_html(source):
    """ Обработка source """
    if isinstance(source, list):
        return render_objects(source)
    return render_obj(source, key_tag=True)


def main():
    with open('source.json') as json_file, JsonLoads():
        source = json.loads(json_file.read(), object_pairs_hook=OrderedDict)
        print(render_html(source))


if __name__ == '__main__':
    main()
