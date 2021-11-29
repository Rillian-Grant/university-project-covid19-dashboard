from flask import Flask, render_template, request

import covid_data_handler, datetime, logging
from schedule_data_updates import DataUpdate, BackgroundDataUpdateHandler

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

data_handler = BackgroundDataUpdateHandler()

@app.route("/healthcheck")
def healthcheck():
    return "OK"

@app.route("/")
@app.route("/index")
def dashboard():
    data = data_handler.dashboard_data()

    #Example: http://127.0.0.1:5000/index?update=23%3A01&two=Test&repeat=repeat&covid-data=covid-data
    # TODO: Fix
    if "two" in request.args:
        print("..........." + request.args["update"])
        if ":" in request.args["update"]:
            # TODO Change to hours and minutes
            [minutes, seconds] = list(map(int, request.args["update"].split(":")))
        else:
            minutes = 5
            seconds = 0
        update_delay = seconds + minutes*60
        update_label = request.args["two"]
        update_repeat = "repeat" in request.args
        update_covid_data = "covid-data" in request.args

        update = DataUpdate(interval=update_delay, label=update_label, repeat=update_repeat, update_covid_data=update_covid_data)
        data_handler.schedule(update)



    return render_template("index.html",
        **data,
        location="Exeter",
        nation_location="England"
    )

if __name__ == "__main__":
    app.run(debug=True)