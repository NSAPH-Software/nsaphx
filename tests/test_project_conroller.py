import unittest
import os
import shutil
import yaml
from nsaphx.project_controller import ProjectController

class TestProjectController(unittest.TestCase):

    def setUp(self):

        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        self.test_dir = os.path.join(current_dir,
                                "test_folder")
        
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

        os.makedirs(self.test_dir)

        self.test_data_dir = os.path.join(current_dir,
                                          "test_data")
        
        if not os.path.exists(self.test_dir):
            raise Exception("test_folder does not exist")
        
        for file in os.listdir(self.test_data_dir):
            file_path = os.path.join(self.test_data_dir, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, self.test_dir)


        # create a project json file. 
        covariate_path = os.path.join(self.test_dir, "covariate.csv")
        exposure_path = os.path.join(self.test_dir, "exposure.csv")
        outcome_path = os.path.join(self.test_dir, "outcome.csv")
        project_params = {
            'name': 'cms_lung_failure',
            'project_id': 20221025,
            'details': {
                'description': 'Computing the effect of longterm pm2.5 exposure on lung cancer.',
                'version': '1.0.0',
                'authors': {
                    'name': 'Naeem Khoshnevis',
                    'email': 'nkhoshnevis@g.harvard.edu'
                }
            },
            'data': {
                'outcome_path': outcome_path,
                'exposure_path': exposure_path,
                'covariate_path': covariate_path
            }
        }

        yaml_content = yaml.dump(project_params, default_flow_style=False)

        with open(os.path.join(self.test_dir, "project.yaml"), "w") as f:
            f.write(yaml_content)

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