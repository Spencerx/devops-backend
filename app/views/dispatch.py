#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, request, current_app
from ..extensions import scheduler
from app.tools.jsonUtils import response_json
from app.tasks.weekly_deploy_report import week_report
from app.tools.apschedulerUtils import get_trigger


dispatch = Blueprint('dispatch', __name__)


@dispatch.route('/')
def tasks():
    """
    调度任务列表
    :return:
    """
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
    with current_app.app_context():
        res = scheduler.get_jobs()
        ret = []
        for job in res:
            print job
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
        return response_json(200, '', ret)


@dispatch.route('/pause', methods=['POST'])
def pausejob():
    """
    暂停任务
    :return:
    """
    json_data = request.get_json()
    job_id = json_data['job_id']
    scheduler.pause_job(job_id, jobstore='default')
    return response_json(200, '', 'pause task {0} success'.format(job_id))


@dispatch.route('/delete', methods=['POST'])
def delete():
    """
    暂停任务
    :return:
    """
    json_data = request.get_json()
    job_id = json_data['job_id']
    scheduler.delete_job(job_id, jobstore='default')
    return response_json(200, '', 'delete task {0} success'.format(job_id))


@dispatch.route('/resume', methods=['POST'])
def resumejob():
    """
    任务恢复
    :return:
    """
    json_data = request.get_json()
    job_id = json_data['job_id']
    scheduler.resume_job(job_id)
    return response_json(200, '', 'pause task {0} success'.format(job_id))


@dispatch.route('/add', methods=['POST'])
def addjob():
    if request.method == 'POST':
        with current_app.app_context():
            args = request.get_json()
            cron = args['cron']
            cron_args = get_trigger(cron)
            job_id = args['job_id']
            scheduler.add_job(func=week_report,
                              id=job_id,
                              trigger='cron',
                              max_instances=1,
                              replace_existing=True,
                              jobstore='default',
                              **cron_args)
            return response_json(200, '', 'job {0} create successful'.format(job_id))
    else:
        return response_json(200, '', '')
