import covid_data_handler

import sched, time, threading, uuid, logging

class BackgroundDataUpdateHandler():
    global_data_store = {
        "covid_data": {
            "local": None,
            "national": None
        },
        "news_data": None
    }
    scheduled_events = []
    scheduler_instance = None
    background_thread_instance = None

    def __init__(self):
        logging.info("Initializing data store")
        self.update_covid_data()

        self.scheduler_instance = sched.scheduler(time.time, time.sleep)

        self.background_thread_instance = threading.Thread(target=self.__background_thread, daemon=True)
        self.background_thread_instance.start()

        logging.info("Started background event handler")

    def update_covid_data(self):
        logging.info("Updating covid data")
        self.global_data_store["covid_data"] = {
            "local": covid_data_handler.covid_API_request(),
            "national": covid_data_handler.covid_API_request(location="England", location_type="nation")
        }
        logging.info("Updated covid data")

    def get_covid_data(self): return self.global_data_store["covid_data"]

    def __background_thread(self):
        while True:
            self.scheduler_instance.run()
    
    def dashboard_data(self):

        def iterate_till_key_not_none(list_of_dicts, key):
            for dict in list_of_dicts:
                if dict[key] != None: return dict[key]


        local_data = self.global_data_store["covid_data"]["local"]
        national_data = self.global_data_store["covid_data"]["national"]

        sorted = {
            "deaths_total": iterate_till_key_not_none(national_data["data"], "cumDeaths28DaysByDeathDate"),
            "hospital_cases": iterate_till_key_not_none(national_data["data"], "hospitalCases"),
            "local_7day_infections": iterate_till_key_not_none(local_data["data"], "newCasesByPublishDateRollingSum"),
            "national_7day_infections": iterate_till_key_not_none(national_data["data"], "newCasesByPublishDateRollingSum")
        }

        return sorted

    def schedule(self, data_update):
        logging.error("Update named {} scheduled for {} seconds in the future".format(data_update.label, data_update.interval))
        self.scheduled_events.append(data_update)
        self.scheduler_instance.enter(
            delay=10,
            priority=0,
            action=self._run_data_update,
            argument=[data_update]
        )

    def _run_data_update(self, data_update):
        print("Running data update")
        if data_update.update_covid_data:
            self.update_covid_data()

        if data_update.repeat:
            self.scheduler_instance.enter(
            delay=data_update.interval,
            priority=0,
            action=self._run_data_update,
            argument=[data_update]
        )
        else:
            self.scheduled_events.remove(data_update)

class DataUpdate:
    uuid = ""
    label = ""
    interval = 0
    repeat = False
    update_covid_data = False
    update_news_data = False
    sched_event_instance = None

    def __init__(self, interval=0, label="Data Update", repeat=False, update_covid_data=False, update_news_data=False):
        self.uuid = uuid.uuid1()
        self.label = label
        self.interval = interval
        self.repeat = repeat
        self.update_covid_data = update_covid_data
        self.update_news_data = update_news_data