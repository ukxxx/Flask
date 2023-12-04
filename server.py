import flask
from flask import request
from dotenv import load_dotenv


load_dotenv()

app = flask.Flask("app")

def hello():
    json_data = request.json
    query_params = request.args
    headers = request.headers
    print(f'{json_data=}')
    print(f'{query_params=}')
    print(f'{headers=}')
    response = flask.jsonify({"hello":"world"})
    return response

app.add_url_rule("/hello", view_func=hello, methods=["POST"])

if __name__ == "__main__":
    app.run(port=8080, debug=True)