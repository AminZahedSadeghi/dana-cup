import pytest
from django.db import connection
from django.conf import settings

# Abstract Django Model for Testing
class AbstractTestModel:
    
    class Meta:
        app_label = settings.FAKE_EN.name()
        db_table = settings.FAKE_EN.name()


# Abstract pytest Test Class for Model Setup/Teardown
class AbstractModelTestCase:
    # def __init__(self):
    #     if not hasattr(self, 'model'):
    #         raise ValueError(f'{self.__class__.__name__} must define a `model` attribute')

    @pytest.fixture(scope="class", autouse=True)
    def setup_class(self, django_db_blocker):
        with django_db_blocker.unblock():
            if not hasattr(self, 'model'):
                pytest.fail(f"{self.__class__.__name__} must define a `model` attribute")

            with connection.schema_editor() as schema_editor:
                schema_editor.connection.in_atomic_block = False
                schema_editor.create_model(self.model)

            # Yield to allow test execution
            yield

            # Teardown after tests finish
            with connection.schema_editor() as schema_editor:
                schema_editor.connection.in_atomic_block = False
                schema_editor.delete_model(self.model)
                schema_editor.connection.in_atomic_block = True
