class QueryCriteria:
    pass

class Where(QueryCriteria):
    def __init__(self, field: str, operator: str, value: any):
        self.field = field
        self.operator = operator
        self.value = value

class OrderBy(QueryCriteria):
    def __init__(self, field: str, direction: str = "ASC"):
        self.field = field
        self.direction = direction