from wtforms import Form, StringField, BooleanField, validators, IntegerField


class FunctionForm(Form):

    func_name = 'transfer'
    gas_limit = 314150

    to = StringField(validators=[validators.DataRequired()])
    amount = IntegerField(validators=[validators.DataRequired()])

    @property
    def contract_data(self):
        return {
            '_to': self.data['to'],
            '_amount': self.data['amount']
        }