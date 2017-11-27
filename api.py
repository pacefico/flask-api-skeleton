from flask import Flask
from flask import jsonify
from flask import abort
from flask import request
from flask import make_response

from utils import tryint, is_user_valid
from decorators import authenticate, check_token, check_error_handler, TOKEN_HEADER_NAME

# create the Flask application
app = Flask(__name__)


def init_api_routes(app_ref):
    """
    Init all endpoints available
    :param app_ref: Flask app reference
    :return: none
    """
    if app_ref:
        # CRUD METHODS
        app_ref.add_url_rule('/api/getbyid/<string:element_id>', 'get_by_id',
                             getbyid, methods=['GET'])
        app_ref.add_url_rule('/api/get', 'get',
                             get, methods=['GET'])
        app_ref.add_url_rule('/api/post', 'add_post',
                             post, methods=['POST'])
        app_ref.add_url_rule('/api/put/<string:element_id>', 'update_by_id',
                             put, methods=['PUT'])
        app_ref.add_url_rule('/api/delete/<string:element_id>', 'delete_by_id',
                             delete, methods=['DELETE'])

        # AUTHENTICATED
        app_ref.add_url_rule('/api/auth', 'auth',
                             page_authentication, methods=['GET'])
        app_ref.add_url_rule('/api/getwithauth', 'get_auth',
                             get_authenticated, methods=['GET'])

        # ERROR HANDLING
        app_ref.add_url_rule('/api/error/<string:element_id>', 'error_handling',
                             error_handler, methods=['GET'])

        # ROOT
        app_ref.add_url_rule('/', 'list_routes',
                             list_routes, methods=['GET'],
                             defaults={'app_ref': app_ref})


def getbyid(element_id):
    """
    Get function with parameter
    :param id: id parameter
    :return: code 200 and json if ok, 404 if id not found
    """
    my_id = tryint(element_id)
    if my_id and my_id in [1, 5, 9, 10]:
        return jsonify({"getbyid": "OK"})
    else:
        abort(404)


def get():
    """
    Get function without  parameter
    :return: code 200 and json ok
    """
    return jsonify({"get": "OK"})


def post():
    """
    Post function to create elements
    :return: code 200 and json if ok, 400 if input request wrong
    """
    my_input = request.form["input"]
    if my_input and my_input == 'input':
        return jsonify({"post": "OK"})
    else:
        abort(400)


def put(element_id):
    """
    Put function to update elements
    :param element_id: id parameter
    :return: code 200 and json if ok, 400 if input invalid, 404 if id not found
    """
    my_id = tryint(element_id)
    if my_id and my_id in [1, 5, 9, 10]:
        put_item = request.form["put"]
        if put_item and put_item == 'put':
            return jsonify({"put": "OK"})
        else:
            abort(400)
    else:
        abort(404)


def delete(element_id):
    """
    Delete function to delete element if found
    :param element_id: id from element to be deleted
    :return: code 200 and json if ok, 404 if id not found
    """
    my_id = tryint(element_id)
    if my_id and my_id in [1, 5, 9, 10]:
        # simulate a delete action here
        return jsonify({"delete": "OK"})
    else:
        abort(404)


@authenticate(is_user_valid_func=is_user_valid)
def page_authentication(*args, **kwargs):
    """
    Authenticate user and password from basic http request
    :param args: args from wrapper function
    :param kwargs: kwargs from wrapper function with token to be returned
    :return: code 200 and json if ok, 401 if authentication fails
    """

    # execute something else here
    resp = make_response(jsonify({"auth": "OK"}), 200)
    resp.headers[TOKEN_HEADER_NAME] = kwargs[TOKEN_HEADER_NAME]
    return resp


@check_token
def get_authenticated():
    """
    Simulate a get function using token authentication
    :return: code 200 and json if ok, 401 if token authentication fails
    """
    return get()


@check_error_handler
def error_handler(element_id):
    print("here")
    my_id = tryint(element_id)
    if my_id and my_id == 1:
        raise Exception("My error throwing an exception")
    else:
        return make_response(jsonify({"Error": "Default error message"}), 500)


def list_routes(app_ref):
    """
    List all routes endpoints
    :param app_ref: flask app reference
    :return: list of routes
    """
    result = []
    for rt in app_ref.url_map.iter_rules():
        result.append({
            'methods': list(rt.methods),
            'route': str(rt)
        })
    return jsonify({'routes': result, 'total': len(result)})


init_api_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
