[![CircleCI](https://circleci.com/gh/atveit/amplitude-python.svg?style=svg&circle-token=dfb7391f33d23ac3dad467b60ca34b36e7a37ebb)](https://circleci.com/gh/atveit/amplitude-python)

# amplitude-python
Python API for Amplitude Analytics Logging - https://amplitude.com

This API is a simple (unofficial) wrapper for the [Amplitude HTTP API](https://amplitude.zendesk.com/hc/en-us/articles/204771828-HTTP-API)

## 1. Install amplitude-python

Potential preparation before installing: create and activate virtualenv or conda environment

### 1.1 Install from pypi with conda or pip
```bash
pip install amplitude-python
```

### 1.2 Install from github
```bash
$ git clone https://github.com/atveit/amplitude-python.git
$ cd amplitude-python
$ python setup.py instal
```

## 2. Logging to Amplitude with amplitude-python

```python
import amplitude

# initialize amplitude logger
amplitude_logger = amplitude.AmplitudeLogger(api_key = "SOME_API_KEY_STRING")

# track an event to amplitude
amplitude_logger.track(device_id="somedeviceid", event_type:"Registration", event_properties={"screen": "First"}, user_properties={"email": "jon@doe.com"})

```

API Reference can be found here – [Amplitude HTTP API Documentation](https://amplitude.zendesk.com/hc/en-us/articles/204771828-HTTP-API) before start logging.

## 3. Test amplitude-python module
```
python setup.py test
```

