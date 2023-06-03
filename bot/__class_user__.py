class User(object):
    _condition = 'no_condition'
    _id = ''

    def change_condition(self, role):
        self._condition = role

    def get_condition(self):
        return self._condition