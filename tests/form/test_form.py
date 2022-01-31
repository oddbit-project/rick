import pytest
from rick.form import Form


class SampleForm(Form):

    def init(self):
        self.field('text', 'name', 'Full Name', validators="required|minlen:4|maxlen:8") \
            .field('text', 'age', 'Age', validators="required|numeric|between:9,125")
        return self


def test_form_simple():
    frm = SampleForm().init()

    # empty data, must fail
    valid = frm.is_valid({})
    assert valid is False

    msgs = frm.error_messages()
    assert len(msgs) is 2
    for id in frm.fields.keys():
        assert id in msgs.keys()

    # age is valid, single error
    valid = frm.is_valid({'age': 32})
    assert valid is False

    msgs = frm.error_messages()
    assert len(msgs) is 1
    assert 'name' in msgs.keys()

    # both fields are valid
    data = {'age': 32, 'name': 'Connor'}
    valid = frm.is_valid(data)
    assert valid is True
    assert len(frm.error_messages()) == 0

    for id in data.keys():
        assert data[id] == frm.get(id)
