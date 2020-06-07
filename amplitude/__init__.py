import requests
import time
import uuid

# The source repo is here - https://github.com/DataGreed/amplitude-python
#

# Documentation of AmplitudeHTTP API:
#   https://developers.amplitude.com/docs/http-api-v2
#
# Convert Curl queries - such as below to - python:
#   https://curl.trillworks.com/
#
# TODO: Example HTTP Curl Query for Amplitude:
#


#
# rate limits
# potentially across multiple machines ...
#


class AmplitudeLogger:
    def __init__(self, api_key, api_uri="https://api.amplitude.com/2/httpapi"):
        self.api_key = api_key
        self.api_uri = api_uri
        self.is_logging = True

        s = self._sess = requests.Session()
        s.headers.update(headers={"Content-Type": "application/json", "Accept": "*/*"})

    def turn_on_logging(self):
        self.is_logging = True

    def turn_off_logging(self):
        self.is_logging = False

    def _is_None_or_not_str(self, value) -> bool:
        return bool(value is None or not isinstance(value, str))

    def create_event_package(self, events, options=None):
        """
        """
        event_package = {
            "api_key": self.api_key,
            "events": events,
        }
        if options:
            event_package["options"] = options
        return event_package

    def create_event(
        self,
        user_id: str = None,
        device_id: str = None,
        event_type: str = None,
        event_properties: dict = None,
        user_properties: dict = None,
        time_ms: float = None,
        min_id_length=None,
        platform: str = None,
        additional_data: dict = None,
    ):
        """
        Creates and returns event payload dictionary. Use log_event to send it.

        :param user_id: (required unless device_id is present) A readable ID specified by you.
        :param device_id: (required unless user_id is present) A device specific identifier,
                          such as the Identifier for Vendor on iOS.
        :param event_type: (required) A unique identifier for your event.
        :param event_properties: A dictionary of key-value pairs that represent additional data to be sent along with the event.
                                 You can store property values in an array,
                                 and date values are transformed into string values.
        :param user_properties: A dictionary of key-value pairs that represent additional data tied to the user.
                                Each distinct value will show up as a user segment on the Amplitude dashboard.
        :param time_ms: The timestamp of the event in milliseconds since epoch. This will update the client event time.
                        If not specified, this value will assume the server upload time by default.
        :return:
        """
        event = {}

        if not user_id and not device_id:
            raise ValueError("Specify either user_id or device_id")

        if device_id:
            event["device_id"] = str(device_id)
        if user_id:
            event["user_id"] = str(user_id)

        if user_properties is not None:
            if isinstance(user_properties, dict):
                event["user_properties"] = user_properties
            else:
                raise ValueError("user_properties must be a dict")

        if self._is_None_or_not_str(event_type):
            raise ValueError("Specify event_type")

        event["event_type"] = event_type

        # integer epoch time in milliseconds
        event["time"] = time_ms or int(time.time() * 1000)

        if platform:
            event["platform"] = platform

        if event_properties:
            if isinstance(event_properties, dict):
                event["event_properties"] = event_properties
            else:
                raise ValueError("event_properties must be a dict")

        # any additional parameters supported by http endpoint
        # see https://help.amplitude.com/hc/en-us/articles/360032842391-HTTP-API-V2
        if isinstance(additional_data, dict):
            event.update(additional_data)

        event['insert_id'] = str(uuid.uuid4())

        return event

    def log_event_package(self, pkg):
        """
        Sends event(s) to amplitude.

        :param event: event payload dictionary
        :return:
        """
        assert pkg, 'Cannot log empty event package'
        if self.is_logging:
            result = self._sess.post(self.api_uri, json=pkg)
            #
            # TODO: handle error codes
            #
            return result

    # def log_event(self, event):
    #     """
    #     Sends event to amplitude. Use create_event to create the payload.
    #     :param event: event payload dictionary
    #     :return:
    #     """
    #     if event:
    #         if self.is_logging:
    #             result = self._sess.post(self.api_uri, json=pkg)
    #             #
    #             # TODO: handle error codes
    #             #
    #             return result
    #     else:
    #         raise Exception("Cannot log empty event")

    def track(
        self,
        user_id=None,
        device_id=None,
        event_type=None,
        event_properties=None,
        user_properties=None,
        time_ms=None,
        min_id_length=None,
        platform=None,
    ):
        """
        Tracks event with specified parameters.

        :param user_id: (required unless device_id is present) A readable ID specified by you.
        :param device_id: (required unless user_id is present) A device specific identifier,
                          such as the Identifier for Vendor on iOS.
        :param event_type: (required) A unique identifier for your event.
        :param event_properties: A dictionary of key-value pairs that represent additional data to be sent along with the event.
                                 You can store property values in an array,
                                 and date values are transformed into string values.
        :param user_properties: A dictionary of key-value pairs that represent additional data tied to the user.
                                Each distinct value will show up as a user segment on the Amplitude dashboard.
        :param time_ms: The timestamp of the event in milliseconds since epoch. This will update the client event time.
                        If not specified, this value will assume the server upload time by default.
        :return:
        """

        options = None
        if min_id_length:
            options = {"min_id_length": min_id_length}

        events = [
            self.create_event(
                user_id=user_id,
                device_id=device_id,
                event_type=event_type,
                event_properties=event_properties,
                user_properties=user_properties,
                time_ms=time_ms,
                min_id_length=min_id_length,
                platform=platform,
            )
        ]

        result = self.log_event_package(
            self.create_event_package(options=options, events=events)
        )

        return result

    def track_batch(self, batch: list):
        #
        # TODO: handle batches larger than 10
        #
        return self.log_event_package(self.create_event_package(events=events))
