from flask import Flask
from random import randint

app = Flask(__name__)


def cpu_intensive():
    return sum([randint(0, i) for i in range(0, 100000)])


@app.route('/')
def hello():
    return 'Hello World!: {}'.format(cpu_intensive())


@app.route('/healthz')
def healthz():
    return 'OK'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
