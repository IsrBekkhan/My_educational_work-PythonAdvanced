from flask import Flask, request, Response

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  {user_input}
</body>
</html>
"""


@app.route('/', methods=['GET'])
def handler():
    """
    URI для проверки:
    http://localhost:8080/?input=<script>alert('HACKED')</script>
    """
    user_input = request.args.get('input', type=str)
    return HTML.format(user_input=user_input), 200


@app.after_request
def add_cors(response: Response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response


if __name__ == '__main__':
    app.run(port=8080, debug=True)


