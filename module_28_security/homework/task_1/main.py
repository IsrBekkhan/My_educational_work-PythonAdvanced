from flask import Flask, jsonify, request, Response

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def handler():
    print(request.headers)
    return jsonify({"Hello": "User"})


@app.after_request
def add_cors(response: Response):
    response.headers['Access-Control-Allow-Origin'] = 'https://www.google.ru'
    response.headers['Access-Control-Allow-Methods'] = 'GET', 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'X-My-Fancy-Header'
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)
