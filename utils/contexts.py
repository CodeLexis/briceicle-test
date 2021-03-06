from flask import g, request

from utils import generate_unique_reference


def get_current_api_ref():
    try:
        return g.api_ref
    except AttributeError:
        g.api_ref = generate_unique_reference()
        return g.api_ref


def get_current_app():
    return g.app


def get_current_request_args():
    return request.args


def get_current_request_data():
    return request.get_json()


def get_current_request_headers():
    return request.headers


def get_current_request_url():
    return request.url


def get_current_user():
    return g.user
