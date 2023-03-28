import unittest
import os
import sys
import io
import tempfile
import shutil
import yaml

from nsaphx.database import Database
from nsaphx.data_node import MainDataNode, DataNode
from nsaphx.base.utils import human_readible_size
from sqlitedict import SqliteDict
from unittest.mock import MagicMock
from nsaphx.project_controller import ProjectController


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
    


if __name__ == "__main__":
    unittest.main()