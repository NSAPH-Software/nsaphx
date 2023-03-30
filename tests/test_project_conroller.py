import unittest
import os
import shutil
import yaml
from nsaphx.project_controller import ProjectController
from tests.setup_test_folders import setup_test_folders

class TestProjectController(unittest.TestCase):

    def setUp(self):

        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.test_dir = setup_test_folders(current_dir, "test_folder")
        self.pc = ProjectController(db_path=os.path.join(self.test_dir,
                                                         "test.db"))

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_create_project(self):
        self.pc.create_project(folder_path=self.test_dir)
        projects_list = self.pc.db.get_value("PROJECTS_LIST")
        self.assertEqual(len(projects_list), 1)

    def test_connect_to_project(self):
        self.pc.create_project(folder_path=self.test_dir)
        self.pc.connect_to_project(folder_path=self.test_dir)
        projects_list = self.pc.db.get_value("PROJECTS_LIST")
        self.assertEqual(len(projects_list), 1)

    def test_remove_project(self):
        self.pc.create_project(folder_path=self.test_dir)
        self.pc.remove_project("cms_lung_failure")
        projects_list = self.pc.db.get_value("PROJECTS_LIST")
        self.assertEqual(len(projects_list), 0)



if __name__ == '__main__':
    unittest.main()