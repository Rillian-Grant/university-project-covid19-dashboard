# university-project-covid19-dashboard

Simple personalised covid information dashboard

## User guide

This program can be run via either:

* The main.py file. N.B. Make sure to run `pip -r requirements.txt` beforehand
* The PyPI package rillian-grant-university-project-covid19-dashboard using the command covid19-dashboard.

WARNING: `config.json` is read from the working directory if the config file is not found a default one is used. If you are using the PyPI version and you want to modify configuration then copy the default config.json from the git repo.

## Known linter errors

* pylint says unsubscriptable-object. Not sure why, the object is definitely subscriptable
* use f string instead of string.format(). I suppressed this one as it's definitely incorrect in context

## Known Issues

* Header image in static folder has no file extension due to template. The full file name is "images"
* Bad formatting on update info. Due to template
* No links on news articles. Due to template
* My api key is hardcoded
