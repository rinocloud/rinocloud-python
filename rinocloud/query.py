


class Query(RinoRequests):
    def __init__(self, dictionary={}, results={'results': 'The query method has not yet been called.'}):
        self.dictionary = dictionary
        self.results = results

    OPERATORS = [
        'lt', 'lte', 'gt', 'gte', 'ne', 'in', 'nin', 'exists', 'or'
    ]

    @classmethod
    def extract_filter_operator(cls, parameter):
        for op in cls.OPERATORS:
            underscored = '__%s' % op
            if parameter.endswith(underscored):
                return parameter[:-len(underscored)], op
        return parameter, None

    def filter(self, **kw):
        for name, value in kw.items():
            attr, operator = Query.extract_filter_operator(name)
            if operator is None:
                self.dictionary[attr] = value
            elif operator is 'or':
                option_list = []
                if '$or' in self.dictionary:
                    option_list = self.dictionary['$or']
                    option_list.append({attr: value})
                    self.dictionary['$' + operator] = option_list
                else:
                    option_list.append({attr: value})
                    self.dictionary['$' + operator] = option_list
            else:
                if attr in self.dictionary:
                    self.dictionary[attr]['$' + operator] = value
                else:
                    self.dictionary[attr] = {'$' + operator: value}
        return self

    def print_filter(self):
        print self.dictionary

    def return_filter(self):
        return self.dictionary

    def remove_filter(self, key=None):
        if key is None:
            self.dictionary = {}
        else:
            self.dictionary.pop(key)

    def query(self):
        response = self.__class__.POST(URI['query'], _json={'query': self.dictionary})
        reply = json_loads_byteified(response._content)
        self.results = []
        for obj in reply['result']:
            self.results.append(Object(Obj_from_dict=obj))
        return self.results
