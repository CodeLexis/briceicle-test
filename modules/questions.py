from flask import render_template, request
from flask.views import MethodView

from app.models import Answer, Question, Unit


class QuestionsRoute(MethodView):
    def get(self):
        return render_template(
            'questions.html',
            units=[unit.as_json() for unit in Unit.query.all()],
            questions=[question.as_json() for question in Question.query.all()]
        )

    def post(self):
        data = request.form

        unit = None

        yes_count = 0

        for question, answer in data.items():
            print(question)
            if question == 'unit':
                unit = Unit(name=answer)
                unit.save()

        for question, answer in data.items():
            question = Question.get(body=question)

            if question:
                Answer(
                    body=answer,
                    question=question,
                    unit=unit).save()

                if answer == 'YES':
                    yes_count += 1

        return 'You scored {}/12'.format(yes_count)
