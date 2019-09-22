from flask import Flask, escape, request
import os

app = Flask(__name__)

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

PORT = int(os.getenv("PORT", "80"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
