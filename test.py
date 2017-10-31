
from jinja2 import Template

def a(**kwargs):
    print kwargs['name']

def b(name, **kwargs):
    t = Template("""
    
    hello,{{name}}
    {%if type==1%}
        {{ age}}
    {% endif %}
    {%if type==2%}
    2
    {% endif %}
    
    """)
    return t.render(name=name, type=kwargs['type'])

print b('bbb', type=1)