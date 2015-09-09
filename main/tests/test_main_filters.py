# coding=utf-8
import mock

from unittest import TestCase
from main.templatetags import main_filters


class AddClassTest(TestCase):
    def test_add_class_returns_fields_as_widget_with_defined_css_class(self):
        field = mock.Mock()
        self.assertEquals(main_filters.add_class(field, 'text-right'), field.as_widget.return_value)
        field.as_widget.assert_called_once_with(attrs={"class": 'text-right'})
