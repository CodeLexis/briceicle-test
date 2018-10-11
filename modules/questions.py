from flask import render_template, request, redirect, session, url_for
from flask.views import MethodView

from app.models import Answer, Question, Unit


class QuestionsRoute(MethodView):
    def get(self):
        if session.get('taken'):
            return redirect(url_for('blueprints.web.results'))

        return render_template(
            'questions.html',
            units=[unit.as_json() for unit in Unit.query.all()],
            questions=[question.as_json() for question in Question.query.all()]
        )

    def post(self):
        data = request.form

        unit = Unit.get(name=data.get('unit'))

        yes_count = 0

        for question, answer in data.items():
            question = Question.get(body=question)

            if question:
                Answer(
                    body=answer,
                    question=question,
                    unit=unit).save()

                if answer == 'YES':
                    yes_count += 1

        session['taken'] = True
        session['score'] = yes_count

        return redirect(url_for('blueprints.web.results', score=yes_count))
