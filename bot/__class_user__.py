class User(object):
    _condition = 'None'
    _id = ''

    def change_condition(self, role):
        if role == 'customer':
            self._condition = 'customer'
        elif role == 'provider':
            self._condition = 'provider'

    def get_condition(self):
        return self._condition
