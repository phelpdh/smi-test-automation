# -*- coding: utf-8 -*-
"""
Power Thermal
~~~~~~~~~~~~~

:Copyright: (c) 2017 DELL Inc. or its subsidiaries.  All Rights Reserved.
:License: Apache 2.0, see LICENSE for more details.
:Author: Akash Kwatra

Created on May 2, 2017
"""

import unittest
import sys
import logging
import config
from resttestms import http, json, log, test, parse

LOG = logging.getLogger(__name__)

# Leave as None to use default Host
HOST_OVERRIDE = None

# Leave as None to use default json directory
DATA_OVERRIDE = None

# Leave as None to use default depth
DEPTH_OVERRIDE = None

def setUpModule():
    """Initialize data for all test cases using overrides"""
    LOG.info("Begin Power Thermal Tests")
    PowerThermalTest.initialize_data(HOST_OVERRIDE, DATA_OVERRIDE, DEPTH_OVERRIDE)

class PowerThermalTest(unittest.TestCase):
    """Collection of data to test the power thermal microservice"""

    PORT = '46019'
    JSON_NAME = 'data_powerthermal.json'

    @classmethod
    def initialize_data(cls, host_override, directory_override, depth_override):
        """Initialize base url, json file path, and depth"""
        cls.HOST = test.select_host(config.HOST, host_override)
        cls.DATA = test.select_directory(config.DATA, directory_override)
        cls.DEPTH = test.select_depth(config.DEPTH, depth_override)
        cls.BASE_URL = test.create_base_url(cls.HOST, cls.PORT)
        cls.JSON_FILE = test.create_json_reference(cls.DATA, cls.JSON_NAME)

###################################################################################################
# Post
###################################################################################################

class Post(PowerThermalTest):
    """Tests for Powerthermal Post Endpoint"""

    ENDPOINT = 'post'

    def test_json(self):
        """POST JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Put
###################################################################################################

class Put(PowerThermalTest):
    """Tests for Put Endpoint"""

    ENDPOINT = 'put'

    def test_json(self):
        """PUT JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# Post All
###################################################################################################

class PostAll(PowerThermalTest):
    """Tests for Powerthermal Post All Endpoint"""

    ENDPOINT = 'post_all'

    def test_json(self):
        """POST ALL JSON TESTS"""
        test.auto_run_json_tests('POST', self)

###################################################################################################
# Put All
###################################################################################################

class PutAll(PowerThermalTest):
    """Tests for Powerthermal Put All Endpoint"""

    ENDPOINT = 'put_all'

    def test_json(self):
        """PUT ALL JSON TESTS"""
        test.auto_run_json_tests('PUT', self)

###################################################################################################
# Version
###################################################################################################

class Version(PowerThermalTest):
    """Tests for Version Endpoint"""

    ENDPOINT = 'version'

    def test_json(self):
        """VERSION JSON TESTS"""
        test.auto_run_json_tests('GET', self)

###################################################################################################
# Test Sequences
###################################################################################################

class TestSequences(PowerThermalTest):
    """Test Sequences for Power Thermal"""

    def test_change_power_cap(self):
        """CHANGE AND CHECK POWER CAP"""
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('PUT', self, Put, "test_server1_415_watts")
        test.run_json_test('POST', self, Post, "test_server1_415_watts")
        test.run_json_test('PUT', self, Put, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server1_401_watts")

    def test_disable_power_cap(self):
        """DISABLE AND ENABLE POWER CAP"""
        test.run_json_test('PUT', self, Put, "test_server1_disable_power_cap")
        test.run_json_test('PUT', self, Put, "test_server1_401_watts")

    def test_multiple_server_power_caps(self):
        """CHANGE AND CHECK MULTIPLE POWER CAPS"""
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server2_200_watts")
        test.run_json_test('POST', self, PostAll, "test_server1_401_watts")
        test.run_json_test('POST', self, PostAll, "test_server2_200_watts")
        test.run_json_test('PUT', self, Put, "test_server1_415_watts")
        test.run_json_test('PUT', self, Put, "test_server2_215_watts")
        test.run_json_test('POST', self, PostAll, "test_server1_415_watts")
        test.run_json_test('POST', self, PostAll, "test_server2_215_watts")
        test.run_json_test('PUT', self, Put, "test_server1_401_watts")
        test.run_json_test('PUT', self, Put, "test_server2_200_watts")
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server2_200_watts")

    def test_distribute_power_cap(self):
        """DISTRIBUTE AND CHECK POWER CAPS"""
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server2_200_watts")
        test.run_json_test('PUT', self, PutAll, "test_server1_and_server2_powercap_404")
        test.run_json_test('POST', self, PostAll, "test_202_and_202_watts")
        test.run_json_test('PUT', self, Put, "test_server1_401_watts")
        test.run_json_test('PUT', self, Put, "test_server2_200_watts")
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server2_200_watts")

    def test_distribute_disable_power_cap(self):
        """DISTRIBUTE AND CHECK POWER CAPS"""
        test.run_json_test('PUT', self, PutAll, "test_server1_and_server2_disable_power_cap")
        test.run_json_test('PUT', self, Put, "test_server1_401_watts")
        test.run_json_test('PUT', self, Put, "test_server2_200_watts")
        test.run_json_test('POST', self, Post, "test_server1_401_watts")
        test.run_json_test('POST', self, Post, "test_server2_200_watts")


###################################################################################################
# RUN MODULE
###################################################################################################

if __name__ == "__main__":
    HOST, DATA, DEPTH = parse.single_microservice_args(sys.argv)
    HOST_OVERRIDE = HOST if HOST else HOST_OVERRIDE
    DATA_OVERRIDE = DATA if DATA else DATA_OVERRIDE
    DEPTH_OVERRIDE = DEPTH if DEPTH else DEPTH_OVERRIDE
    log.configure_logger_from_yaml('logs/logger_config.yml')
    unittest.main()
