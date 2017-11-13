#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_apscheduler import APScheduler
from apscheduler.jobstores.redis import RedisJobStore
from flask import Flask, request, jsonify
from app.tools.apschedulerUtils import get_trigger


class Config(object):
    JOBS = []
    SCHEDULER_JOBSTORES = {
        'default': RedisJobStore(host='localhost', port=6379)
    }
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 1
    }
    SCHEDULER_API_ENABLED = True


scheduler = APScheduler()
app = Flask(__name__)
app.config.from_object(Config())
scheduler.init_app(app)


def job1(a, b):
    print '==aaaaa===='


# def jobfromparm(name):
#     job = scheduler.add_job(func=func,id=id, args=args,trigger=trigger,seconds=seconds)
#     return 'sucess'

@app.route('/pause')
def pausejob():
    scheduler.pause_job('first_inter_job_3')
    return "Success!"


@app.route('/resume')
def resumejob():
    scheduler.resume_job('first_inter_job_3')
    return "Success!"


@app.route('/list')
def listjob():
    """
    Contains the options given when scheduling callables and its current schedule and other state.
    This class should never be instantiated by the user.

    :var str id: the unique identifier of this job
    :var str name: the description of this job
    :var func: the callable to execute
    :var tuple|list args: positional arguments to the callable
    :var dict kwargs: keyword arguments to the callable
    :var bool coalesce: whether to only run the job once when several run times are due
    :var trigger: the trigger object that controls the schedule of this job
    :var str executor: the name of the executor that will run this job
    :var int misfire_grace_time: the time (in seconds) how much this job's execution is allowed to
        be late
    :var int max_instances: the maximum number of concurrently executing instances allowed for this
        job
    :var datetime.datetime next_run_time: the next scheduled run time of this job

    .. note::
        The ``misfire_grace_time`` has some non-obvious effects on job execution. See the
        :ref:`missed-job-executions` section in the documentation for an in-depth explanation.

    :return:
    """
    res = scheduler.get_jobs()
    for job in res:
        print job.id
        print job.args
        print job.kwargs
        print job.coalesce
        print type(job.trigger)
        print job.executor
        print job.misfire_grace_time
        print job.max_instances
        print job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        print job.max_instances
    return 'list'


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    number1 = 1
    number2 = 6
    cron = get_trigger('* * * * * * * */2')
    cron_args = {
        'year': '*',
        'month': '*',
        'day': '*',
        'week': '*',
        'day_of_week': '*',
        'hour': '17',
        'second': '00',
        'minute': '53',
    }
    job = scheduler.add_job(func=job1, id='first_inter_job_3', args=(number1, number2),
                            trigger='cron',
                            replace_existing=True,
                            **cron)
    print 'add'
    print job
    return 'add ok '


if __name__ == '__main__':
    scheduler.start()
    app.run(host='0.0.0.0', port=18888, debug=True)

