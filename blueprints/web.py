from flask import Blueprint

from modules import QuestionsRoute, ResultsRoute


web_blueprint = Blueprint(__name__, 'web_blueprint', url_prefix='')


mappings = [
    ('/questions', QuestionsRoute, 'questions'),
    ('/results', ResultsRoute, 'results'),
]


for url in mappings:
    path, view, name = url

    web_blueprint.add_url_rule(path, view_func=view.as_view(name))
