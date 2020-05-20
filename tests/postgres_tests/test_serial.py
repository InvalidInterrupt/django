from django.core.management.color import no_style
from django.db import connection
from django.test.utils import modify_settings

from . import PostgreSQLTestCase
from .models import BigSerialTestModel, SerialTestModel, SmallSerialTestModel


@modify_settings(INSTALLED_APPS={'append': 'django.contrib.postgres'})
class SerialFieldTestCase(PostgreSQLTestCase):
    target_model = SerialTestModel

    def test_sequence(self):
        for i in range(1,6,2):
            self.assertEqual(self.target_model.objects.create(value=i).value, i)
        for i in range(1,3):
            self.assertEqual(self.target_model.objects.create().value, i)
        with connection.cursor() as cursor:
            for command in connection.ops.sequence_reset_sql(no_style(), [self.target_model]):
                cursor.execute(command)
        self.assertEqual(self.target_model.objects.create().value, 6)


class BigSerialFieldTestCase(SerialFieldTestCase):
    target_model = BigSerialTestModel


class SmallSerialFieldTestCase(SerialFieldTestCase):
    target_model = SmallSerialTestModel
