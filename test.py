from collections import OrderedDict

from convector import render_html
from unittest import TestCase, main
import json


class UnitTest(TestCase):
    """
    Тест-кейс для 3-5 задач из тестового задания. 
    1 и 2 задача не подходят для тестирование по результатам, 
    которые предоставлены в тестовом задании в качестве проверки, 
    так как было внесено существенное изменение в 3 задаче
    по поводу отображения списков в обертке тегов ul-li.
    
    Но в последующих задачах достигнута обратная совместимость по результатам из примеров.
    """

    def setUp(self):
        self.data_3 = (
            '[{"h3": "Title #1","div": "Hello, World 1!"},{"h3": "Title #2","div": "Hello, World 2!"}]',
            '<ul><li><h3>Title #1</h3><div>Hello, World 1!</div></li><li><h3>Title #2</h3><div>Hello, '
            'World 2!</div></li></ul>'
        )
        self.data_4_1 = (
            '[{"span": "Title #1","content": [{"p": "Example 1","header": "header 1"}]},{"div": "div 1"}]',
            '<ul><li><span>Title #1</span><content><ul><li><p>Example 1</p><header>header 1</header></li></ul>'
            '</content></li><li><div>div 1</div></li></ul>'
        )
        self.data_4_2 = (
            '{"p":"hello1"}', '<p>hello1</p>'
        )
        self.data_5 = (
            '{"p.my-class#my-id": "hello","p.my-class1.my-class2":"example<a>asd</a>"}',
            '<p id="my-id" class="my-class">hello</p><p class="my-class1 my-class2">example&lt;a&gt;asd&lt;/a&gt;</p>'
        )

    def tearDown(self):
        del self.data_3
        del self.data_4_1
        del self.data_4_2
        del self.data_5

    @staticmethod
    def json_loads(data):
        return json.loads(data, object_pairs_hook=OrderedDict)

    def test_three(self):
        test_data, res = self.data_3
        self.assertEqual(render_html(self.json_loads(test_data)), res)

    def test_fourth_list(self):
        test_data, res = self.data_4_1
        self.assertEqual(render_html(self.json_loads(test_data)), res)

    def test_fourth_one_obj(self):
        test_data, res = self.data_4_2
        self.assertEqual(render_html(self.json_loads(test_data)), res)

    def test_five(self):
        test_data, res = self.data_5
        self.assertEqual(render_html(self.json_loads(test_data)), res)


if __name__ == '__main__':
    main()


# Запуск тестов с подробным отчетом
# python -m unittest -v test.py
