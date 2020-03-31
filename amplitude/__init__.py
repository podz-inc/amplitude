import requests
import time
import json

# Original implementation borrowed
# from https://github.com/abinba/amplitude-python

# Documentation of AmplitudeHTTP API:
#   https://amplitude.zendesk.com/hc/en-us/articles/204771828
#
# Convert Curl queries - such as below to - python:
#   https://curl.trillworks.com/
#
# Example HTTP Curl Query for Amplitude:
#   curl --data 'api_key=SOMEIDOFAKIND' --data 'event=[{"user_id":"john_doe@gmail.com", "event_type":"watch_tutorial", "user_properties":{"Cohort":"Test A"}, "country":"United States", "ip":"127.0.0.1", "time":1396381378123}]' https://api.amplitude.com/httpapi


class AmplitudeLogger:
    def __init__(self, api_key, api_uri="https://api.amplitude.com/2/httpapi"):
        self.api_key = api_key
        self.api_uri = api_uri
        self.is_logging = True

    def turn_on_logging(self):
        self.is_logging = True

    def turn_off_logging(self):
        self.is_logging = False

    def _is_None_or_not_str(self, value):
        if value is None or type(value) is not str:
            return True

    def create_event(self, user_id=None, device_id=None, event_type=None, event_properties=None,
                     user_properties=None, time_ms=None):
        event = {}

        if self._is_None_or_not_str(user_id) or self._is_None_or_not_str(device_id):
            raise ValueError("Specify either user_id or device_id")
        else:
            event["device_id"] = device_id
            event["user_id"] = user_id

        if user_properties is not None:
            if type(user_properties) == dict:
                event["user_properties"] = user_properties
            else:
                raise ValueError("user_properties must be a dict")

        if self._is_None_or_not_str(event_type):
            raise ValueError("Specify event_type")

        event["event_type"] = event_type

        # integer epoch time in milliseconds
        if time_ms:
            event["time"] = time_ms
        else:
            # current time
            event["time"] = int(time.time() * 1000)

        if event_properties:
            if type(event_properties) == dict:
                event["event_properties"] = event_properties
            else:
                raise ValueError("event_properties must be a dict")

        event_package = {
            'api_key': self.api_key,
            'events': [event]
        }

        return event_package

    def log_event(self, event):
        if event is not None:
            if self.is_logging:
                result = requests.post(self.api_uri, json=event)
                return result
