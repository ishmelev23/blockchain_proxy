from wtforms import Form, StringField, BooleanField, validators


class ActionForm(Form):

    name = StringField(validators=[validators.DataRequired()])
    testbool = BooleanField(validators=[validators.DataRequired()])