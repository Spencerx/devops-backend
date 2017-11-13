import opentracing
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracer
from flask import Flask, jsonify

log_level = logging.DEBUG
logging.getLogger('').handlers = []
logging.basicConfig(format='%(asctime)s %(message)s', level=log_level)


class Configb(object):
    DEFAULT_REPORTING_HOST = '192.168.15.255'
    DEFAULT_REPORTING_PORT = 5775
    DEFAULT_SAMPLING_PORT = 5778
    LOCAL_AGENT_DEFAULT_ENABLED = True


config = Config(
    config={
        'sampler': {
            'type': 'const',
            'param': 1,
        },
        'logging': True,
        'DEFAULT_REPORTING_HOST': '192.168.15.255',
        'DEFAULT_REPORTING_PORT': 5775,
        'DEFAULT_SAMPLING_PORT': 5778,
        'LOCAL_AGENT_DEFAULT_ENABLED': True,
    },
    service_name='devops-redis-product',
)
# this call also sets opentracing.tracer
tracer = config.initialize_tracer()
app = Flask(__name__)
app.config.from_object(Configb())

opentracing_tracer = tracer
tracer = FlaskTracer(opentracing_tracer, True, app)


@app.route('/product')
@tracer.trace()
def index():
    import redis
    r = redis.Redis()
    r.incr('uber')
    sp = opentracing_tracer.start_span('hello')
    tracer.inject(span_context=sp.context())
    sp.finish()
    return jsonify({'data': r.get('uber')})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11111)
