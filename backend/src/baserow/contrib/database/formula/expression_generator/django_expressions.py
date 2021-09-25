from django.db.models import Transform


# noinspection PyAbstractClass
class BinaryOpExpr(Transform):
    template = "%(expressions)s"
    arity = 2


# Django provides no way of doing a SQL equals expression with an arbitrary Django
# expression on both the LHS and RHS. Instead we have to define our own simple transform
# which joins two expressions together with a single =.
# noinspection PyAbstractClass
class EqualsExpr(BinaryOpExpr):
    arg_joiner = "="


# noinspection PyAbstractClass
class NotEqualsExpr(BinaryOpExpr):
    arg_joiner = "!="


# noinspection PyAbstractClass
class GreaterThanExpr(BinaryOpExpr):
    arg_joiner = ">"


# noinspection PyAbstractClass
class GreaterThanOrEqualExpr(BinaryOpExpr):
    arg_joiner = ">="


# noinspection PyAbstractClass
class LessThanExpr(BinaryOpExpr):
    arg_joiner = "<"


# noinspection PyAbstractClass
class LessThanEqualOrExpr(BinaryOpExpr):
    arg_joiner = "<="


# noinspection PyAbstractClass
class AndExpr(BinaryOpExpr):
    arg_joiner = " AND "


# noinspection PyAbstractClass
class OrExpr(BinaryOpExpr):
    arg_joiner = " OR "


# noinspection PyAbstractClass
class NotExpr(Transform):
    template = "not %(expressions)s"
    arity = 1
