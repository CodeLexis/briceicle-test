from flask import render_template, request, redirect, url_for
from flask import session
from flask.views import MethodView

from app.models import Answer, Question, Unit


class ResultsRoute(MethodView):
    def get(self):
        score = request.args.get('score') or session.get('score') or 12

        questions = [question.as_json() for question in Question.query.all()]

        return render_template(
            'results.html',
            questions=questions,
            score=score
        )
