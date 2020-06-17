from flask import Flask, abort, request

app = Flask(__name__)

@app.route('/greet')
def greet():
    api_key = request.args.get('api_key')
    if api_key == 'example-api-key':
        return "Hello, World!"
    else:
        abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
