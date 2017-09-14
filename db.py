from peewee import *

database = MySQLDatabase('devops', **{'host': '127.0.0.1', 'password': 'admin', 'port': 3306, 'user': 'root'})

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
    create_time = DateTimeField()
    t = PrimaryKeyField(db_column='t_id')
    team_leader = CharField(null=True)
    team_name = CharField()
    team_status = IntegerField()

    class Meta:
        db_table = 'teams'

class Users(BaseModel):
    can_approved = IntegerField()
    email = CharField()
    is_active = CharField()
    name_pinyin = CharField(null=True)
    password = CharField(null=True)
    role = IntegerField()
    username = CharField()

    class Meta:
        db_table = 'users'

class Workflow(BaseModel):
    access_info = CharField(null=True)
    approved_user = IntegerField(null=True)
    close_time = DateTimeField(null=True)
    comment = CharField(null=True)
    config = CharField(null=True)
    create_time = DateTimeField()
    create_user = CharField()
    current_version = CharField()
    deny_info = CharField(null=True)
    deploy_info = CharField(null=True)
    dev_user = IntegerField()
    last_version = CharField(null=True)
    ops_user = IntegerField(null=True)
    production_user = IntegerField()
    service = CharField()
    sql_info = CharField(null=True)
    status = IntegerField()
    team_name = IntegerField()
    test_user = IntegerField()
    w = PrimaryKeyField(db_column='w_id')

    class Meta:
        db_table = 'workflow'

