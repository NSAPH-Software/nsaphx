import os
import shutil
import yaml


def setup_test_folders(current_dir, test_folder_name):
        current_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        test_dir = os.path.join(current_dir,
                                test_folder_name)
        
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

        os.makedirs(test_dir)

        test_data_dir = os.path.join(current_dir,
                                     "test_data")
        
        if not os.path.exists(test_dir):
            raise Exception("test_folder does not exist")
        
        for file in os.listdir(test_data_dir):
            file_path = os.path.join(test_data_dir, file)
            if os.path.isfile(file_path):
                shutil.copy(file_path, test_dir)


        # create a project json file. 
        covariate_path = os.path.join(test_dir, "covariate.csv")
        exposure_path = os.path.join(test_dir, "exposure.csv")
        outcome_path = os.path.join(test_dir, "outcome.csv")
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

        with open(os.path.join(test_dir, "project.yaml"), "w") as f:
            f.write(yaml_content)

        return test_dir