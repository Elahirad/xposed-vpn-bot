"""Peewee migrations -- 005_added server and product models.py.

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


with suppress(ImportError):
    import playhouse.postgres_ext as pw_pext


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""
    
    @migrator.create_model
    class Server(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        name = pw.CharField(max_length=255, unique=True)
        url = pw.CharField(max_length=255, unique=True)
        proxy_path = pw.CharField(max_length=255)
        admin_uuid = pw.CharField(max_length=255)

        class Meta:
            table_name = "servers"

    @migrator.create_model
    class Product(pw.Model):
        id = pw.BigIntegerField(primary_key=True)
        name = pw.CharField(max_length=255, unique=True)
        server = pw.ForeignKeyField(column_name='server_id', field='id', model=migrator.orm['servers'], on_delete='RESTRICT')
        days = pw.BigIntegerField()
        gb_limit = pw.BigIntegerField()
        price = pw.BigIntegerField()

        class Meta:
            table_name = "products"


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""
    
    migrator.remove_model('servers')

    migrator.remove_model('products')
