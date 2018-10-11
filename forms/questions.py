from flask_wtf import Form
from wtforms import BooleanField, PasswordField, StringField
from wtforms import IntegerField, SubmitField, TextAreaField, FileField
from wtforms import validators


class CreateAppForm(Form):
    unit = TextAreaField('Unit', [
        validators.Length(10),
        validators.DataRequired()
    ])

    image = FileField('App Icon')
    privacy_policy_url = StringField('Privacy policy url', [
        validators.URL()
    ])
    url = StringField('URL', [
        validators.URL()
    ])
    webhook_url = StringField('Webhook URL', [
        validators.URL()
    ])
    submit = SubmitField("SUBMIT")
