from peewee import *

database = MySQLDatabase('devops', **{'host': '127.0.0.1', 'password': 'admin', 'port': 3306, 'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Bugs(BaseModel):
    exception_info = CharField()
    flow = IntegerField(db_column='flow_id')

    class Meta:
        db_table = 'bugs'

class Deploy(BaseModel):
    deploy_script = TextField(null=True)
    deploy_time = DateTimeField()
    is_locked = IntegerField()
    workflow = IntegerField()

    class Meta:
        db_table = 'deploy'

class FlowType(BaseModel):
    type = CharField()

    class Meta:
        db_table = 'flow_type'

class Roles(BaseModel):
    r = PrimaryKeyField(db_column='r_id')
    role_name = CharField()

    class Meta:
        db_table = 'roles'

class Scripts(BaseModel):
    comment = CharField(null=True)
    script_content = TextField(null=True)
    script_name = CharField(null=True)
    type = CharField(null=True)

    class Meta:
        db_table = 'scripts'

class Servers(BaseModel):
    hostname = CharField(null=True)
    internal_ip = CharField()
    outernal_ip = CharField(null=True)
    ssh_passwd = CharField()
    ssh_port = IntegerField()
    ssh_user = CharField()
    type = CharField()

    class Meta:
        db_table = 'servers'

class ServiceBackend(BaseModel):
    comment = CharField(null=True)
    port = IntegerField(null=True)
    server = IntegerField(db_column='server_id', index=True, null=True)
    service = IntegerField(db_column='service_id', index=True, null=True)

    class Meta:
        db_table = 'service_backend'

class Services(BaseModel):
    comment = CharField(null=True)
    create_time = DateTimeField()
    current_version = CharField(null=True)
    deploy_script = IntegerField(null=True)
    deploy_script_template = IntegerField(null=True)
    first_approve_user = IntegerField(null=True)
    is_switch_flow = IntegerField()
    language = CharField(null=True)
    s = PrimaryKeyField(db_column='s_id')
    second_approve_user = IntegerField(null=True)
    service_leader = IntegerField()
    service_name = CharField()
    service_status = CharField()
    type = CharField(null=True)

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
    can_approved = CharField()
    create_time = DateTimeField(null=True)
    email = CharField()
    is_active = CharField()
    is_admin = CharField()
    name = CharField(null=True)
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
    current_version = CharField(null=True)
    deny_info = CharField(null=True)
    deploy_info = CharField(null=True)
    deploy_script_name = CharField(null=True)
    deploy_time = DateTimeField(null=True)
    dev_user = IntegerField(null=True)
    is_except = IntegerField()
    last_version = CharField(null=True)
    ops_user = IntegerField(null=True)
    production_user = IntegerField(null=True)
    service = CharField(null=True)
    sql_info = CharField(null=True)
    status = IntegerField()
    team_name = IntegerField()
    test_user = IntegerField()
    type = IntegerField()
    w = PrimaryKeyField(db_column='w_id')

    class Meta:
        db_table = 'workflow'

