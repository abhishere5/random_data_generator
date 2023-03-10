from flask import Flask, jsonify, Response
import matplotlib
import scipy.stats as stats
import math
import io
import random
import numpy as np
from flask_cors import CORS
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)


@app.route('/normal/<int:mean>/<int:sd>/<int:num>')
def norm(mean, sd, num):
    data = normal(mean, sd, num)
    return jsonify(data)


@app.route('/normal_graph/<int:mean>/<int:sd>/<int:num>')
def plot_png(mean, sd, num):
    data = normal(mean, sd, num)
    fig = Figure()
    x = data['data']

    axis = fig.add_subplot()

    n, bins, patches = axis.hist(x, num, density=True, color='red')
    y = ((1 / (np.sqrt(2 * np.pi) * sd)) *
         np.exp(-0.5 * (1 / sd * (bins - mean)) ** 2))
    axis.plot(bins, y, '--', color='black')
    axis.set_xlabel('X-Axis')
    axis.set_ylabel('Y-Axis')

    axis.set_title('Normal distribution')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/normal_graph_comp/<int:mean>/<int:sd>/<int:num>')
def plot_png1(mean, sd, num):
    data = stats.norm.rvs(size=num, loc=0, scale=10)
    fig = Figure()

    axis = fig.add_subplot()

    n, bins, patches = axis.hist(data, num, density=True, color='red')
    y = ((1 / (np.sqrt(2 * np.pi) * sd)) *
         np.exp(-0.5 * (1 / sd * (bins - mean)) ** 2))
    axis.plot(bins, y, '--', color='black')
    axis.set_xlabel('X-Axis')
    axis.set_ylabel('Y-Axis')

    axis.set_title('Normal distribution Generated by Scipy module')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def normal(mean, sd, num):
    data = []
    for i in range(num):
        u1 = random.random()
        u2 = random.random()
        x1 = math.sqrt(-2 * math.log2(u1))
        x2 = math.cos(2 * math.pi * u2)
        z = x1 * x2
        data.append(mean + (sd * z))

    return {'data': data}

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)