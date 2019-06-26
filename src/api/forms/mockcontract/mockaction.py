from wtforms import Form, StringField, BooleanField, validators


class FunctionForm(Form):

    func_name = 'Function1'
    gas_limit = 140000

    name = StringField(validators=[validators.DataRequired()])
    testbool = BooleanField(validators=[validators.DataRequired()])