from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__) # server creation
app.config['SECRET_KEY'] = "secret" # configuring key
app.debug = True

debug = DebugToolbarExtension(app)

RES_KEY = "responses"
survey = satisfaction_survey

@app.route('/') # @ is decorator
def home_page():
    return render_template('start.html', survey=survey)

@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """Save response and redirect to next question."""

    # get the response choice
    choice = request.form['answer']

    # add this response to the session
    responses = session[RES_KEY]
    responses.append(choice)
    session[RES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """Display current question."""
    responses = session.get(RES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qid):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")