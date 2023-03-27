import json
import hashlib
from abc import ABC, abstractmethod
from nsaphx.plugin_registery import PLUGIN_MAP
from nsaphx.database import Database
import os
from nsaphx.base.utils import human_readible_size
import re
import pandas as pd

class DataClass(ABC):

    @abstractmethod
    def _add_hash(self):
        pass

    @abstractmethod
    def apply(self, instruction):
        pass

    @abstractmethod
    def summary(self):
        pass

    @abstractmethod
    def check_data(self):      
        pass    

    @abstractmethod
    def apply(self, instruction):
        pass



class MainDataNode(DataClass):
    def __init__(self, project_params, db_path):
        self.project_params = project_params
        self.input_data = None
        self._add_hash()
        self._create_data_attribute()
        self.descendant_hash = []
        self.hash_by_type = dict()
        self.db_path = db_path
        self._connect_to_database()

    def _create_data_attribute(self):
        exposure_path = self.project_params.get("data").get("exposure_path")
        outcome_path = self.project_params.get("data").get("outcome_path")
        covariate_path = self.project_params.get("data").get("covariate_path")
        self.data = {"path":{"outcome_path": outcome_path,
                             "exposure_path": exposure_path,
                             "covariate_path": covariate_path},
                     "d_index": None, 
                     "d_generated": dict()}
        
    def _add_hash(self):
        hash_string = self.project_params["hash_value"] + "MainDataNode"
        try:            
            self.hash_value =  hashlib.sha256(
                hash_string.encode('utf-8')).hexdigest()
        except Exception as e:
            print(e) 

    def summary(self):
        print(f"Main data node hash: {self.hash_value}")
        print(f"    Data: {self.data}")
        print(f"    All child hash: {self.descendant_hash}")
        print(f"    Hash by type: {self.hash_by_type}")


    def data_summary(self):
        self.check_data()
        for key, value in self.data["path"].items():
            print(f"{re.sub('_path', '', key)}:")
            key_data = pd.read_csv(value)
            print(f"    Number of rows: {key_data.shape[0]}")
            print(f"    Number of columns: {key_data.shape[1]}")
            print(f"    Column names: {key_data.columns.tolist()}")
            print(f"    First 5 rows:")
            print(key_data.head())

    def access_data(self, data_name = None):
        
        if data_name is None:
            data = {}
            for key, value in self.data["path"].items():
                _key = f"{re.sub('_path', '', key)}"
                loaded_data = pd.read_csv(value)
                data[_key] = loaded_data
        else:
            pass

        return data



    def _connect_to_database(self):
        if self.db_path is None:
            raise Exception("No database path provided.")
        
        self.db = Database(self.db_path)

    def get_data_node(self, hash_value):
        return self.db.get_value(hash_value)
    
    def check_data(self):
        for key, value in self.data["path"].items():
            print(f"Working on {key} : {value} ...")
            file_exist = os.path.exists(value)
            print(f"    File accessible: {file_exist}")
            if file_exist:
                file_size = human_readible_size(os.path.getsize(value))
                print(f"    File size: {file_size}")

    def apply(self, instruction):
        # Generates a new lazy node and put's it in the data.base.
        
        plugin_name = instruction.get("plugin_name")
        plugin_function = PLUGIN_MAP.get(plugin_name)

        # First create a new data node
        # Then apply the plugin function to the data node

        if plugin_function is not None:
            data_node = DataNode(self.hash_value, instruction,
                                 db_path=self.db_path)
            data_node.input_data = self.data
            self.descendant_hash.append(data_node.hash_value)
            self.hash_by_type[plugin_name] = data_node.hash_value
            self.db.set_value(data_node.hash_value, data_node)
            return data_node
        else:
            raise ValueError(f"Plugin {plugin_name} not found.")
        
    def __str__(self):
        return (f"{self.__class__.__name__}(hash_value={self.hash_value}," + 
                f" db_path={self.db_path})")



class DataNode(DataClass):
    def __init__(self, parent_node_hash, instruction, db_path):
        self.input_data = None
        self.output_data = None
        self.computed = False
        self.hash_value = None
        self.parent_node_hash = parent_node_hash
        self.instruction = instruction
        self.db_path = db_path
        self.descendant_hash = []
        self.hash_by_type = dict()
        self._connect_to_database()
        self._update_input_data()
        self._add_hash()

    def _add_hash(self):
        hash_string = (self.parent_node_hash + 
                       json.dumps(self.instruction, sort_keys=True))
        
        self.hash_value = hashlib.sha256(
            hash_string.encode('utf-8')).hexdigest()
   
    def apply(self, instruction):
        # Generates a new lazy node and put's it in the data.base.
        if not self.computed:
            Warning("The data node has not been computed yet. ")
            return

        plugin_name = instruction.get("plugin_name")
        plugin_function = PLUGIN_MAP.get(plugin_name)

        # First create a new data node
        # Then apply the plugin function to the data node

        if plugin_function is not None:
            data_node = DataNode(self.hash_value, instruction,
                                 db_path=self.db_path)
            data_node.input_data = self.output_data
            self.descendant_hash.append(data_node.hash_value)
            self.hash_by_type[plugin_name] = data_node.hash_value
            self.db.set_value(data_node.hash_value, data_node)
            return data_node
        else:
            raise ValueError(f"Plugin {plugin_name} not found.")
        

    def summary(self):
        pass

    def compute(self):
        if self.computed is False:
            
            # compute
            self.computed = True
            plugin_name = self.instruction.get("plugin_name")
            plugin_function = PLUGIN_MAP.get(plugin_name)
            
            if plugin_function is not None:
                output_data = plugin_function(self.input_data, self.instruction)
                # sanity check to see if output data has required keys.
                self.output_data = output_data
                self.update_node_on_db()
            else:
                raise ValueError(f"Plugin {plugin_name} not found.")
            

        else:
            print(f"The data node has already been computed." +
                  f"Run .reset() to reset the node.")
            
    def reset(self):
        self.computed = False
        self.data = self.parent_node.data


    def _update_input_data(self):
        pass

    def _connect_to_database(self):
        if self.db_path is None:
            raise Exception("No database path provided.")
        
        self.db = Database(self.db_path)

    def update_node_on_db(self):
        self.db.set_value(self.hash_value, self)
    
    
    def check_data(self):
        for key, value in self.input_data["path"].items():
            print(f"Working on {key} : {value} ...")
            file_exist = os.path.exists(value)
            print(f"    File accessible: {file_exist}")
            if file_exist:
                file_size = human_readible_size(os.path.getsize(value))
                print(f"    File size: {file_size}")

    def access_input_data(self):
        pass

    def access_output_data(self):
        pass





    