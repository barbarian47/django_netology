from datetime import datetime


class PubDateConverter:
    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    date_format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.strptime(value, self.date_format)

    def to_url(self, value):
        return value.strftime(self.date_format)