import json
import urllib.error
import urllib.request

from flask import render_template, Blueprint, request, session
from markupsafe import Markup

predict_page = Blueprint('predict_page', __name__)


@predict_page.route('/', methods=["GET", "POST"])
def _index():
    if request.method == 'POST':
        # HERE DOWN TO TRY STATEMENT - Azure Machine Learning Supplied code
        # Variables (E.g. Room_Number) request form data from HTML page and assign it to itself
        data = {
            "Inputs": {
                "input1":
                    [
                        {
                            'Room_Number': request.form['Room Number'],
                            'Weekday': request.form['Weekday'],
                            'Month': request.form['Month'],
                            'Hour': request.form['Hour'],
                            'Minutes': request.form['Minutes'],
                        }
                    ],
            },
            "GlobalParameters": {
            }
        }

        body = str.encode(json.dumps(data))

        url = 'https://japaneast.services.azureml.net/workspaces/8933a6cd0fc0472f85cc6780697fb118/services/897e4a8c5ebe4c6681bd81e33d7b8116/execute?api-version=2.0&format=swagger'
        api_key = '/wc9LKDQcH8wtQ3OtfhkF/Z8dLjWcJZvP3BrP6vWKnertrmFBxOXRrPBeAOGjksN64DrJ3H5H2i2xSJY97Pzrw=='  # Replace this with the API key for the web service
        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            # Get a response from the Azure API, decode it into utf-8, load result into json format for accesibility ease
            response = urllib.request.urlopen(req)
            result = response.read().decode("utf-8")
            json_result = json.loads(result)

            # Allocate all json variable results to matching python variables to be used
            # Allocate session ID's to variables to save drop-down states between submissions
            room_number = json_result['Results']['output1'][0]['Room_Number']
            session['Room Number'] = room_number

            scored_probability = float(json_result['Results']['output1'][0]['Scored Probabilities'])
            scored_label = int(json_result['Results']['output1'][0]['Scored Labels'])

            weekday = json_result['Results']['output1'][0]['Weekday']
            session['Weekday'] = weekday

            month = json_result['Results']['output1'][0]['Month']
            session['Month'] = month

            hour = int(json_result['Results']['output1'][0]['Hour'])
            # Hour session is set when setting meridians and 12-hour so it can be displayed nicely

            minutes = json_result['Results']['output1'][0]['Minutes']
            session['Minutes'] = minutes

            # Convert probability to percentage, flip 0 labels to be correct percentage, set colour of text based on occupancy
            if scored_label == 0:
                scored_probability = (1 - scored_probability) * 100
                scored_label = "<font color='green'>un-occupied</font>"
            if scored_label == 1:
                scored_probability *= 100
                scored_label = "<font color='red'>occupied</font>"

            # Set a meridan to display, convert hour to 12-hour format if necessary, format session to display nicely
            if hour > 12:
                meridian = "PM"
                hour -= 12
                session['Hour'] = f"{str(hour)} {meridian}"
            else:
                meridian = "AM"
                session['Hour'] = f"{str(hour)} {meridian}"

            # Set minutes to have a double 0 to make result string look better for straight hour times, less confusing to look at
            if minutes == "0":
                minutes = "00"

            # Formatted result string based on all variables / calculations to be displayed to the user
            result_string = Markup(
                f"Room <b>{room_number}</b> has a "
                f"<b>{scored_probability:.2f}%</b> chance to be "
                f"<b>{scored_label}</b> on a "
                f"<b>{weekday}</b> in "
                f"<b>{month}</b> at "
                f"<b>{hour}:{minutes} {meridian}</b>")

            # Return the result string to the HTML page to be displayed
            return render_template("predict_page.html", result=result_string)

        # Catch any HTTP errors
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))
        return render_template("predict_page.html")
    return render_template("predict_page.html")
