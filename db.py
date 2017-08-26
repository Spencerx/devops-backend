from peewee import *

database = MySQLDatabase('devops', **{'host': '192.168.234.132', 'password': 'admin', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Roles(BaseModel):
    r = PrimaryKeyField(db_column='r_id')
    role_name = CharField()

    class Meta:
        db_table = 'roles'

class Services(BaseModel):
    s = PrimaryKeyField(db_column='s_id')
    service_name = CharField()
    war_url = CharField(null=True)

    class Meta:
        db_table = 'services'

class Status(BaseModel):
    s = PrimaryKeyField(db_column='s_id')
    status_info = CharField()

    class Meta:
        db_table = 'status'

class Teams(BaseModel):
    t = PrimaryKeyField(db_column='t_id')
    team_name = CharField()

    class Meta:
        db_table = 'teams'

class Users(BaseModel):
    is_active = CharField()
    password = CharField()
    role = IntegerField()
    username = CharField()

    class Meta:
        db_table = 'users'

class Workflow(BaseModel):
    approved_user = IntegerField(null=True)
    close_time = DateTimeField(null=True)
    comment = CharField(null=True)
    create_time = DateTimeField()
    current_version = CharField()
    deploy_info = CharField(null=True)
    dev_user = IntegerField()
    last_version = CharField(null=True)
    ops_user = IntegerField()
    production_user = IntegerField()
    service = CharField()
    sql_info = CharField(null=True)
    status = IntegerField()
    team_name = IntegerField()
    test_user = IntegerField()
    w = PrimaryKeyField(db_column='w_id')

    class Meta:
        db_table = 'workflow'

