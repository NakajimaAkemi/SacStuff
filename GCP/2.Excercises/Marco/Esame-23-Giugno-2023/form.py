from wtforms import Form, TextAreaField, validators

class ipForm(Form):
    ip = TextAreaField('Cerca un IP', [validators.length(min=0, max=255)])