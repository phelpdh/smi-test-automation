# -*- coding: utf-8 -*-
"""
Test Toolkit
~~~~~~~~~~~~
Series of tools designed to control testing

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on June 28, 2017
"""

import logging
from . import json, http, log, parse

LOG = logging.getLogger(__name__)

###################################################################################################
# Premade Tests
###################################################################################################

@log.exception(LOG)
def get_bad_data(end_class):
    """Run GET requests with missing or empty data, check for failure"""
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        response = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def post_bad_data(end_class):
    """Run POST requests with missing or empty data, check for failure"""
    for combo in _bad_data_combos(json.get_base_payload(end_class)):
        response = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def get_bad_data_except(end_class, good_combos):
    """Run GET requests with missing or empty data excluding those specified, check for failure"""
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        response = http.rest_get(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, "<= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def post_bad_data_except(end_class, good_combos):
    """Run POST requests with missing or empty data excluding those specified, check for failure"""
    for combo in _bad_data_combos_except(json.get_base_payload(end_class), good_combos):
        response = http.rest_post(end_class.URL, combo)
        with end_class.subTest(data=combo):
            end_class.assertTrue(has_status_code(response, ">= 400"), "Expected Response Code : 400")

@log.exception(LOG)
def get_json(end_class):
    """Run tests specified in JSON using GET requests"""
    print("")
    for test_case in json.get_all_tests(end_class):
        skip, description, payload, expected = json.parse_test(end_class, test_case)
        if skip:
            print(skip)
        else:
            response = http.rest_get(end_class.URL, payload)
            with end_class.subTest(test=description):
                end_class.assertTrue(compare_response(response, expected), "Bad Response")

@log.exception(LOG)
def post_json(end_class):
    """Run tests specified in JSON using POST requests"""
    print("")
    for test_case in json.get_all_tests(end_class):
        skip, description, payload, expected = json.parse_test(end_class, test_case)
        if skip:
            print(skip)
        else:
            response = http.rest_post(end_class.URL, payload)
            with end_class.subTest(test=description):
                end_class.assertTrue(compare_response(response, expected), "Bad Response")

###################################################################################################
# Test Data Generators
###################################################################################################

def _bad_data_combos(payload):
    """Generate all combinations of empty and missing data"""
    for empty_combo in http.empty_data_combos(payload):
        yield empty_combo
    for incomplete_combo in http.missing_data_combos(payload):
        yield incomplete_combo

def _bad_data_combos_except(payload, good_combos):
    """Generate all combinations of empty and missing data except for those specified"""
    for bad_combo in _bad_data_combos(payload):
        valid_bad_combo = True
        for good_combo in good_combos:
            if set(good_combo) == set(bad_combo.keys()):
                valid_bad_combo = False
        if valid_bad_combo:
            yield bad_combo

###################################################################################################
# Test Results
###################################################################################################

def has_status_code(response, status):
    """Check if response status code is less than, greater than, or equal to specifed code"""
    operation, code = parse.status_code(status)
    LOG.debug("Checking Response Status Code :: Expected : %s %s Actual : %s", operation, code, response.status_code)
    if operation == '=' or operation == '==':
        return response.status_code == code
    elif operation == '>':
        return response.status_code > code
    elif operation == '<':
        return response.status_code < code
    elif operation == '>=':
        return response.status_code >= code
    elif operation == '<=':
        return response.status_code <= code

def compare_response(response, exp_data):
    """
    Compare specified values in expected with those in response
    If status_code is specified, compare with response status code as well
    """
    exp_status_code = None
    if "STATUS_CODE" in exp_data:
        exp_status_code = exp_data["STATUS_CODE"]
    if exp_status_code:
        if response.status_code != exp_status_code:
            LOG.error("============ BAD RESPONSE ============ :: Expected status code : %s Actual Status Code : %s",
                      exp_status_code, response.status_code)
            return False
    exp_response_dict = {key: exp_data[key] for key in exp_data if key != "STATUS_CODE"}
    response_dict = json.make_response_dict(response)
    for key in exp_response_dict:
        if key in response_dict:
            if exp_response_dict[key] == response_dict[key]:
                continue
            else:
                LOG.error("============ BAD RESPONSE ============ :: Key: %s Expected : %s Actual : %s",
                          key, exp_response_dict[key], response_dict[key])
                return False
        else:
            LOG.error("============ BAD RESPONSE ============ :: Expected key \"%s\" not contained in response", key)
            return False
    return True
