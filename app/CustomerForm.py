from wtforms import Form, BooleanField, StringField, PasswordField, validators

class customerform(Form):
    name = StringField('name', [validators.Length(min=4, max=255,message='Name should be between 4 and 255 caharacter'),validators.DataRequired(message='name filed is required')])
    email = StringField('email', [validators.Length(min=6, max=35),validators.DataRequired(message='email filed is required'),validators.Email(message='invalid email format')])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.Regexp('^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$',message='Minimum eight characters, at least one upper case English letter, one lower case English letter, one number and one special character')
    ])