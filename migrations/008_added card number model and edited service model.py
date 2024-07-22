"""Peewee migrations -- 008_added card number model and edited service model.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['table_name']            # Return model in current state by name
    > Model = migrator.ModelClass                   # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.run(func, *args, **kwargs)           # Run python function with the given args
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.add_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)
    > migrator.add_constraint(model, name, sql)
    > migrator.drop_index(model, *col_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.drop_constraints(model, *constraints)

"""

from contextlib import suppress

import peewee as pw
from peewee_migrate import Migrator
import datetime


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    migrator.add_fields(
        'services',

        is_test_service=pw.BooleanField(default=False),
        created_at=pw.DateTimeField(default=datetime.datetime.now()))

    @migrator.create_model
    class Card(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        number = pw.CharField(max_length=255)
        is_active = pw.BooleanField()

        class Meta:
            table_name = "cards"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_fields('services', 'is_test_service', 'created_at')

    migrator.change_fields('services', server=pw.ForeignKeyField(column_name='server_id', default=1, field='id', model=migrator.orm['servers'], on_delete='RESTRICT'),
        product=pw.ForeignKeyField(column_name='product_id', default=1, field='id', model=migrator.orm['products'], on_delete='RESTRICT'))

    migrator.remove_model('cards')
