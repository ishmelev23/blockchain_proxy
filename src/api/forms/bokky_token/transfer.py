from wtforms import Form, StringField, BooleanField, validators, IntegerField


class FunctionForm(Form):

    func_name = 'transfer'
    gas_limit = 314150

    _to = StringField(validators=[validators.DataRequired()])
    _amount = IntegerField(validators=[validators.DataRequired()])