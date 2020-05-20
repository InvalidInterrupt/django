from django.core import checks
from django.db.models import BigIntegerField, Expression, IntegerField, SmallIntegerField

__all__ = ['BigSerialIntegerField', 'SerialIntegerField', 'SmallSerialIntegerField']


class SerialIntegerField(IntegerField):
    db_returning = True
    uses_sequence = True

    class DefaultValueExpression(Expression):
        def as_sql(self, compiler, connection):
            raise NotImplementedError("Only supported on PostgreSQL")

        def as_postgresql(self, compiler, connection):
            return "DEFAULT", []

    def __init__(self, *args, **kwargs):
        kwargs["blank"] = True
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["blank"]
        return name, path, args, kwargs

    def db_type(self, connection):
        return "serial"

    def check(self, **kwargs):
        return [*super().check(**kwargs), *self._check_not_null()]

    def _check_not_null(self):
        if self.null:
            return [checks.Error(
                'Serial Fields cannot be nullable.',
                obj=self,
                id='postgres.E004'
            )]
        else:
            return []

    def get_db_prep_save(self, value, connection):
        value = super().get_db_prep_save(value, connection)
        return value if value is not None else self.DefaultValueExpression()


class BigSerialIntegerField(SerialIntegerField, BigIntegerField):
    def db_type(self, connection):
        return "bigserial"


class SmallSerialIntegerField(SerialIntegerField, SmallIntegerField):
    def db_type(self, connection):
        return "smallserial"
