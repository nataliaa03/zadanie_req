import requests
import pytest
import json
import logging
from request_methods import RequestsMethods
from test_data import BASE_URL, APP_ID, EXISTING_APP_JSON, APP_NAME, APP_TYPE, NEW_APP_JSON, APP_TO_PATCH_JSON, APP_TO_PATCH_JSON_INVALID, PATCH_TYPE_JSON, NOT_EXISTING_ID, DEFAULT_LIMIT, INVALID_NAME_APP_JSON, INVALID_TYPE_APP_JSON, INVALID_ID

# @pytest.mark.api
# def test_healthchecks_api():
#     headers = {'Content-Type': 'application/json'}
#     url = 'http://10.243.5.2/apps/'
#     response = requests.get(url=url, headers=headers)
#     assert response.status_code == 200

request_methods = RequestsMethods()


############## GET apps ####################

#testing GET apps request with default paramteres - without passing parameters in URL adress
#verify if limit parameter works correctly
@pytest.mark.tc1a
def test_default_params():
    response = request_methods.get_apps(None, None, None) #default values of offset and limit (1 nad 5)
    json_data = response.json()
    assert len(list(json_data[0].keys())) == DEFAULT_LIMIT
    assert response.status_code == 200

#testing GET apps request with valid paramters of offset, limit and search and no search (9 configurations of paramters in total)
#verify the status code 200
@pytest.mark.tc1b
@pytest.mark.parametrize("offset", [1, 99])
@pytest.mark.parametrize("limit", [1, 99])
@pytest.mark.parametrize("search", ["F", None])
def test_valid_offset_and_limit(offset, limit, search):
    response = request_methods.get_apps(offset, limit, search) #the thrid paramter of search is set to None - no search option
    assert response.status_code == 200

#testing GET apps request - verify if elements of the response (keys) are correct
@pytest.mark.tc1c
def test_elements_of_get_apps_response():
    response = request_methods.get_apps(1, 1)
    json_data = response.json()
    assert list(json_data[0].keys()) == ['name', 'type', 'urls', 'id', 'created_at']


#testing GET apps request - verify if the offset parameter works correctly - getting elements with shifted offsets and comparing responses
@pytest.mark.tc1d
def test_offset():
    response_offset_1 = request_methods.get_apps(1, 5)
    response_offset_3 = request_methods.get_apps(3, 5)
    json_data_offset_1 = response_offset_1.json()
    json_data_offset_3 = response_offset_3.json()
    assert json_data_offset_1[3] == json_data_offset_3[1]


#testing GET apps request - verify if invalid data results in status 422
@pytest.mark.tc1e
def test_invalid_request_422():
    headers = {'Content-Type': 'application/json'}
    url = BASE_URL + 'invalid_req'
    response = requests.get(url=url, headers=headers)
    assert response.status_code == 422

#testing GET apps request - verify if invalid data - limit out of range results in status 422
#verify if the message is expected
@pytest.mark.tc1f
def test_limit_out_of_range():
    response = request_methods.get_apps(1, 999)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "ensure this value is less than 100"
    assert message == expected_message
    assert response.status_code == 422

#testing GET apps request - verify if invalid data - offset=0 results in status 422
#verify if the message is expected
@pytest.mark.tc1g
def test_offset_out_of_range():
    response = request_methods.get_apps(0, 4)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "ensure this value is greater than 0"
    assert message == expected_message
    assert response.status_code == 422



############## POST Create App | DELETE Delete App ####################

#to not load and leave the db with test data - testing POST Create App and DELETE Delete App are in one TEST CASE
#verify POST and DELETE statuses
@pytest.mark.tc2a
def test_create_app_valid_data():
    response = request_methods.create_app(NEW_APP_JSON)
    json_data = response.json()
    assert response.status_code == 200

    #teardown - deleting created app by id
    id_of_created_app = json_data["id"]
    response2 = request_methods.del_app_by_id(id_of_created_app)
    assert response2.status_code == 204

#testing POST Create App - creating app with existing name
#verify status and expected message
@pytest.mark.tc2b
def test_create_existing_app():
    response = request_methods.create_app(EXISTING_APP_JSON)
    json_data = response.json()
    message = json_data["detail"]
    expected_message = "App with given name already exists"
    assert message == expected_message
    assert response.status_code == 400

#testing POST Create App - creating app with too long name (over 60 chars)
#verify status and expected message
@pytest.mark.tc2c
def test_create_app_invalid_name():
    response = request_methods.create_app(INVALID_NAME_APP_JSON)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "ensure this value has at most 60 characters"
    assert message == expected_message
    assert response.status_code == 422

#testing POST Create App - creating app with invalid type
#verify status and expected message
@pytest.mark.tc2d
def test_create_app_invalid_type():
    response = request_methods.create_app(INVALID_TYPE_APP_JSON)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "value is not a valid enumeration member; permitted: 'web', 'mobile', 'sharepoint'"
    assert message == expected_message
    assert response.status_code == 422


#testng DELETE request by passing not existing ID
#verify DELETE status code and message
@pytest.mark.tc2e
def test_delete_app_not_existing_id():
    response = request_methods.del_app_by_id(NOT_EXISTING_ID)
    json_data = response.json()
    message = json_data["detail"]
    expected_message = "App with given id does not exist"
    assert message == expected_message
    assert response.status_code == 400

#testing DELETE app request - passing invalid ID - not uuid format
#verify status code and message
@pytest.mark.tc2f
def test_delete_app_by_not_existing_id():
    response = request_methods.del_app_by_id(INVALID_ID)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "value is not a valid uuid"
    assert message == expected_message
    assert response.status_code == 422



##############  GET app by id ####################

#testing status code for GET app request
@pytest.mark.tc3a
def test_get_app_by_id_status_code():
    response = request_methods.get_app_by_id(APP_ID)
    json_data = response.json()
    assert response.status_code == 200

#testing GET app request - verifying ID
@pytest.mark.tc3b
def test_get_app_by_id_correct_id():
    response = request_methods.get_app_by_id(APP_ID)
    json_data = response.json()
    assert json_data["id"] == APP_ID

#testing GET app request - passing not existing ID (valid uuid format)
#verify status code and message
@pytest.mark.tc3c
def test_get_app_by_not_existing_id():
    response = request_methods.get_app_by_id(NOT_EXISTING_ID)
    json_data = response.json()
    message = json_data["detail"]
    expected_message = "App with given id not found"
    assert message == expected_message
    assert response.status_code == 404

#testing GET app request - passing invalid ID - not uuid format
#verify status code and message
@pytest.mark.tc3d
def test_get_app_by_not_existing_id():
    response = request_methods.get_app_by_id(INVALID_ID)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "value is not a valid uuid"
    assert message == expected_message
    assert response.status_code == 422




##############  PATCH Update App ####################

#to not update existing data and not load the data base - this Test includes creating a new app, patching and delete afer test
#testng PATCH request with valid json payload
#verify status status_code
#deleting the app and verify status of delete
@pytest.mark.tc4a
def test_patch_app_valid_id():
    #1 create app
    response = request_methods.create_app(NEW_APP_JSON)
    json_data = response.json()

    #2 patch created app by its id
    id_of_created_app = json_data["id"]
    response2 = request_methods.patch_app_by_id(id_of_created_app, APP_TO_PATCH_JSON)
    assert response2.status_code == 200

    #teardown - deleting created app by id
    response3 = request_methods.del_app_by_id(id_of_created_app)
    assert response3.status_code == 204


#testing PATCH with not complete payload - including only one value (missing fields)
#verify status code and message
#deleting the app and verify status of delete
@pytest.mark.tc4b
def test_patch_only_type():
    #1 create app
    response = request_methods.create_app(NEW_APP_JSON)
    json_data = response.json()
    assert response.status_code == 200

    #2 patch created app by its id
    id_of_created_app = json_data["id"]
    response2 = request_methods.patch_app_by_id(id_of_created_app, PATCH_TYPE_JSON)
    json_data2 = response2.json()
    message2 = json_data2["detail"][0]["msg"]
    expected_message2 = "field required"
    assert message2 == expected_message2
    assert response2.status_code == 422

    #teardown - deleting created app by id
    response3 = request_methods.del_app_by_id(id_of_created_app)
    assert response3.status_code == 204


#testing PATCH with not existing app ID
#verify status code and message
@pytest.mark.tc4c
def test_patch_app_():
    response = request_methods.patch_app_by_id(NOT_EXISTING_ID, APP_TO_PATCH_JSON)
    json_data = response.json()
    message = json_data["detail"]
    expected_message = "App with given id does not exist"
    assert message == expected_message
    assert response.status_code == 400


#testing PATCH with not valid payload (invalid type)
#verify status code and message
@pytest.mark.tc4d
def test_patch_app_invalid_type():
    response = request_methods.patch_app_by_id(NOT_EXISTING_ID, APP_TO_PATCH_JSON_INVALID)
    json_data = response.json()
    message = json_data["detail"][0]["msg"]
    expected_message = "value is not a valid enumeration member; permitted: 'web', 'mobile', 'sharepoint'"
    assert message == expected_message
    assert response.status_code == 422


# @pytest.mark.tc101
# def test_emergency_deleting():
#     response = request_methods.del_app_by_id("4b773669-5a16-4385-a3f6-3f51e76bdb05")
#     assert response.status_code == 204
