import unittest
import os
import sys
import io
import tempfile
import shutil

from nsaphx.database import Database
from nsaphx.data_node import MainDataNode, DataNode
from nsaphx.base.utils import human_readible_size
from sqlitedict import SqliteDict
from unittest.mock import MagicMock


class TestMainDataNode(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, 'test_db.sqlite')

        self.project_params = {
            "hash_value": "test_hash",
            "data": {
                "exposure_path": "path/to/exposure.csv",
                "outcome_path": "path/to/outcome.csv",
                "covariate_path": "path/to/covariate.csv"
            }
        }
        self.main_data_node = MainDataNode(self.project_params, self.db_path)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_create_data_attribute(self):
        expected_data = {
            "path": {
                "exposure_path": "path/to/exposure.csv",
                "outcome_path": "path/to/outcome.csv",
                "covariate_path": "path/to/covariate.csv"
            },
            "d_index": None
        }
        self.assertEqual(self.main_data_node.input_data, expected_data)

    def test_add_hash(self):
        expected_hash = 'b79241446601f67d508cc77804a8cabfbda9ba9a9dc43a60b19faabc683fd1bf'
        self.assertEqual(self.main_data_node.hash_value, expected_hash)

    def test_connect_to_database(self):
        self.assertIsNotNone(self.main_data_node.db)

    
class TestDataNode(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.test_dir, 'test_db.sqlite')

        self.project_params = {
            "hash_value": "test_hash",
            "data": {
                "exposure_path": "path/to/exposure.csv",
                "outcome_path": "path/to/outcome.csv",
                "covariate_path": "path/to/covariate.csv"
            }
        }
        self.main_data_node = MainDataNode(self.project_params, self.db_path)

        self.instruction = {
            "plugin_name": "example_plugin",
            "plugin_params": {"param1": "value1", "param2": "value2"}
        }
        self.data_node = DataNode(self.main_data_node.hash_value, self.instruction, self.db_path)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_add_hash(self):
        expected_hash = '73c02e56c9fe3868749995f8821f5a087545e7bc98adcf03b80a4e2ac2e73bf7'
        self.assertEqual(self.data_node.hash_value, expected_hash)

    def test_connect_to_database(self):
        self.assertIsNotNone(self.data_node.db)



if __name__ == "__main__":
    unittest.main()