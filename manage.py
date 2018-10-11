#! /usr/bin/env python
import os

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import db
from app.models import Question, Status, Unit
from wsgi import application


manager = Manager(application)


if os.environ['RUNNING_MODE'] == 'development':
    migrate = Migrate(application, db, directory='local_migrations')

else:
    migrate = Migrate(application, db, directory='remote_migrations')


manager.add_command('db', MigrateCommand)


@manager.command
def pump_units_table():
    print('units')

    units = [
        'Integrations',
        'UI/UX',
        'Mobile',
        'Network',
        'Systems'
    ]

    for unit in units:
        Unit(name=unit).save()


@manager.command
def pump_questions_table():
    print('questions')

    questions = [
        'Do you have regular 1:1 meetings?',
        'Do engineering managers code less than 20% of the time?',
        'Are engineering processes measured and continuously improved (e.g. '
        'on-boarding, development, deployment, etc)?',
        'Are bugs, technical debt and refactoring tracked and openly '
        'discussed?',
        'Does senior management view addressing technical debt as an ongoing '
        'and necessary process?',
        'Are mistakes expected, and experiments encouraged, to allow the team '
        'to learn (i.e. psychological safety)?',
        'Are there clear, documented engineering practices & values the team '
        'lives by?',
        'Does the team estimate work regularly?',
        'Does the team influence hiring decisions?',
        'Are poor performers dealt with effectively?',
        'Can engineers interact with users/customers?',
        'Are the QA engineers integrated with the development teams?'
    ]

    for question in questions:
        try:
            Question(body=question).save()
        except:
            pass


@manager.command
def pump_statuses_table():
    print('statuses')

    status_modes_and_ids = {
        'Active': 1,
        'Pending': 2,
        'Disabled': 3,
        'Failed': 4,
        'Blocked': 13,
        'Deleted': 99
    }

    for status, id_ in status_modes_and_ids.items():
        if Status.get(name=status) is not None:
            continue

        status = Status(name=status)
        status.save()

        try:
            status.update(id=id_)
        except:
            pass


@manager.command
def run_all_commands():
    pump_statuses_table()
    pump_units_table()
    pump_questions_table()


if __name__ == "__main__":
    manager.run()
