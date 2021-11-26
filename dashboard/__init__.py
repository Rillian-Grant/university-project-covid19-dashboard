from flask import Flask, render_template

import covid_data_handler
from schedule_data_updates import DataUpdate, BackgroundDataUpdateHandler

app = Flask(__name__)

data_handler = BackgroundDataUpdateHandler()

@app.route("/healthcheck")
def healthcheck():
    return "OK"

@app.route("/")
@app.route("/index")
def dashboard():
    data = data_handler.dashboard_data()

    return render_template("index.html",
        **data,
        location="Exeter",
        nation_location="England"
    )

if __name__ == "__main__":
    app.run(debug=True)