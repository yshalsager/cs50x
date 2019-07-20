import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get("name")
    device = request.form.get("device")
    payment = request.form.get("payment")
    # check inputs
    if not name:
        return render_template("error.html",
                               message="You must enter your Full Name!")
    elif len(name.strip()) == 0:
        return render_template("error.html",
                               message="Your Full Name must not contain blank values!")
    elif not device:
        return render_template("error.html", message="You must select a device!")
    elif not payment:
        return render_template("error.html", message="You must select a payment method!")
    # Once input is validated write it to csv file
    with open('survey.csv', 'a') as fh:
        writer = csv.writer(fh)
        writer.writerow((name, device, payment))
    return redirect('/sheet')  # Redirect user to sheet.html


@app.route("/sheet", methods=["GET"])
def get_sheet():
    # Open survey.csv file and load it
    with open('survey.csv', 'r') as input:
        reader = csv.reader(input)
        surveys = list(reader)
    return render_template("sheet.html", surveys=surveys)
