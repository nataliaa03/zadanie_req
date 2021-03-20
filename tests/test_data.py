import json

BASE_URL  = r'http://10.243.5.2/apps/'
DEFAULT_LIMIT = 5

#existing in app - to GET tests
APP_ID = "0acb8433-8963-4b02-9d71-4e8102e8bc70"
APP_NAME = "Ancient Forest"
APP_TYPE = "sharepoint"


EXISTING_APP_JSON = json.dumps(
    {
      "name": "Ancient Forest",
      "type": "sharepoint",
      "urls": [
        "https://irrelevant.com"
      ]
    }
)


# not existing - to POST, DELETE, PUT tests:
NEW_APP_JSON = json.dumps(
    {
      "name": "Pretty App Test",
      "type": "web",
      "urls": [
        "https://pretty_app_test1.com",
        "http://pretty_app_test2.com",
        "http://pretty.pl"
      ]
    }
)


INVALID_NAME_APP_JSON = json.dumps(
    {
      "name": "Application with too long name - more than 60 characted in the name lllllllllllllllllllllllllllllll",
      "type": "web",
      "urls": [
        "https://pretty_app_test1.com",
        "http://pretty_app_test2.com",
        "http://pretty.pl"
      ]
    }
)

INVALID_TYPE_APP_JSON = json.dumps(
    {
      "name": "Application with wrong type",
      "type": "webapp",
      "urls": [
        "https://pretty_app_test1.com",
        "http://pretty_app_test2.com",
        "http://pretty.pl"
      ]
    }
)



# for PATCH tests:

APP_TO_PATCH_JSON = json.dumps(
    {
      "name": "Patched App Test",
      "type": "mobile",
      "urls": [
        "http://pretty_app_patched.com",
        "http://pretty_app_patched2.com"
      ]
    }
)

APP_TO_PATCH_JSON_INVALID = json.dumps(
    {
      "name": "Patched App Test",
      "type": "invalid_type",
      "urls": [
        "http://pretty_app_patched.com",
        "http://pretty_app_patched2.com"
      ]
    }
)


PATCH_TYPE_JSON = json.dumps(
    {
      "type": "sharepoint"
    }
)



# not existing id
NOT_EXISTING_ID = "0acb8433-8963-4b02-9d71-4e8102e8bc99"

#not uuid id
INVALID_ID = "222"
