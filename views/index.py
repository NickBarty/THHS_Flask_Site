import json
import urllib.error
import urllib.request

from flask import render_template, Blueprint

index = Blueprint('index', __name__)


@index.route('/')
def _index():
    data = {
        "Inputs": {
            "input1":
                [
                    {
                        'Room_Number': "",
                        'Weekday': "",
                        'Month': "",
                        'Hour': "1",
                        'Minutes': "1",
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
        response = urllib.request.urlopen(req)

        result = response.read()

        # Return this to website
        print(result)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
    return render_template("index.html")
