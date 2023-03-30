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
from tests.setup_test_folders import setup_test_folders


class TestMainDataNode(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.test_dir = setup_test_folders(current_dir, "test_folder")
        self.pc = ProjectController(db_path=os.path.join(self.test_dir,
                                                         "test.db"))
        self.pc.create_project(folder_path=self.test_dir)
        self.pc.connect_to_project(folder_path=self.test_dir)        
        pr = self.pc.get_project("cms_lung_failure")
        self.main_data_node = MainDataNode(pr.project_params, pr.db_path)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_data_attribute(self):
        self.assertEqual(len(self.main_data_node.input_data["d_index"]), 600)
        keys = ["exposure_path", "outcome_path", "covariate_path"]
        for key in keys:
            self.assertIn(key, self.main_data_node.input_data["path"])                        
     
    def test_add_hash(self):
        expected_hash = 'b378cf64443561b82c52381d3a8c5740674ce16adc14ecdfad90d7919f2d77b7'
        self.assertEqual(self.main_data_node.hash_value, expected_hash)

    def test_connect_to_database(self):
        self.assertIsNotNone(self.main_data_node.db)

if __name__ == "__main__":
    unittest.main()