from flask import Flask, render_template, request

import covid_data_handler, datetime, logging
from data_handler import DataUpdate, BackgroundDataUpdateHandler

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

    # TODO: Fix
    if "two" in request.args:
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
    
    if "update_item" in request.args:
        event_to_remove = filter(lambda i: i.label == request.args["update_item"], data_handler.scheduled_events)
        for event in event_to_remove:
            data_handler.remove(event)

    if "notif" in request.args:
        data_handler.remove_news_article(request.args["notif"])

    # Update data
    updates = []
    for event in data_handler.scheduled_events:
        updates.append({
            "title": event.label,
            "content": str(event)
        })


    return render_template("index.html",
        **data,
        location="Exeter",
        nation_location="England",
        updates=updates
    )

if __name__ == "__main__":
    app.run(debug=True)