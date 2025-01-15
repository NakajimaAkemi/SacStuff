from wtforms import Form, TextAreaField, validators

class messageForm(Form):
    message = TextAreaField('Inserisci un messaggio', [validators.length(min=2, max=255)])
    
class hashtagForm(Form):
    hashtag = TextAreaField('Cerca un hashtag', [validators.length(min=2, max=255)])