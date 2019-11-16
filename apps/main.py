#!/usr/bin/python3
# coding: utf-8

# Requirements
# Flask and sysmpy must be installed from pip.

# Import modules
from flask import Flask, render_template, request
import math
import sys
import sympy

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolve', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        frombpm = request.form['from']
        tobpm = request.form['to']

        # Check values
        if frombpm == "":
            error = "Error: The original BPM is not specified."
            return render_template('index.html', error=error)
        elif tobpm == "":
            error = "Error: The target BPM is not specified."
            return render_template('index.html', error=error)

        try:
            frombpm = float(frombpm)
        except ValueError:
            error = "Error: The values must be integer or float."
            return render_template('index.html', error=error)

        try:
            tobpm = float(tobpm)
        except ValueError:
            error = "Error: The values must be integer or float."
            return render_template('index.html', error=error)

        if frombpm == tobpm:
            error = "Error: Same value specified."
            return render_template('index.html', error=error)

        # Main process
        deltabpm = tobpm - frombpm
        if request.form['options'] == "1":
            plist = [round(i * 0.02, 2) for i in range(1, 302)]
        elif request.form['options'] == "2":
            plist = [round(i * 0.5, 2) for i in range(1, 202)]

        pitch = ((round((tobpm / frombpm - 1) * 100, 4)))
        proot = math.sqrt(pow(pitch, 2))
        pdict = {}

        for i in plist:
            delta = math.sqrt(pow(i - proot, 2))
            pdict[i] = delta

        sortedpitch = sorted(pdict.items(), key=lambda x: x[1])
        answer = sortedpitch[0][0]
        if request.form['options'] == "1":
            if answer > 6.0:
                error = "Error: Out of range.(-6% ~ +6%)"
                return render_template('index.html', error=error)
        elif request.form['options'] == "2":
            if answer > 10.0:
                error = "Error: Out of range.(-10% ~ +10%)"
                return render_template('index.html', error=error)

        if deltabpm <= 0:
            percentage = "Pitch: -{}%".format(answer)
            actual = frombpm / (answer / 100 + 1)

        else:
            percentage = "Pitch: +{}%".format(answer)
            actual = frombpm * (answer / 100 + 1)

        notice = "Actual BPM: {}".format(actual)
        source = "{} --> {}".format(frombpm, tobpm)

        return render_template('index.html', source=source, percentage=percentage, notice=notice)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
