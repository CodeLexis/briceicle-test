from flask import Blueprint, request

from modules import QuestionsRoute, ResultsRoute


web_blueprint = Blueprint(__name__, 'web_blueprint', url_prefix='')


@web_blueprint.route('/echo-headers')
def echo_headers():
    return str(request.headers)


mappings = [
    ('/', QuestionsRoute, 'questions_'),
    ('/questions', QuestionsRoute, 'questions'),

    ('/results', ResultsRoute, 'results'),
]


for url in mappings:
    path, view, name = url

    web_blueprint.add_url_rule(path, view_func=view.as_view(name))
