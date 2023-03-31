Quickstart
==========

Installing the Package
----------------------

1. Install the package using pip

.. code-block:: bash

   pip install nsaphx


2. Install the package from source

.. code-block:: bash

   git clone https://github.com/NSAPH-Software/nsaphx
   cd nsaphx
   pip install .

Usage
-----

The process can be defined in the following steps:

Create a project controller instance
++++++++++++++++++++++++++++++++++++

The ProjectController is the main controller for the project. In the following we will describe how to use it. All projects can be on the same database. The project controller instance needs a path to the database. The database is a sqlite database. If the database does not exist, it is created automatically.

.. code-block:: python 
    >>> from nsaphx.project_controller import ProjectController
    >>> pc = ProjectController('test_database.sqlite')

The `pc` object has a list of available projects on the database. The list is empty at the beginning.

.. code-block:: python 
    >>> pc.summary()
    Number of projects in the database: 0

Create a project instance
+++++++++++++++++++++++++

A project is a folder (with an arbitrary name) that contains a `project.yaml` file. The following keys are required in the `project.yaml` file:

- `name`: The name of the project. 
- `id`: The id of the project (any integer number).
- `data`: Which includes following keys:
  - `outcome_path`: The path to the outcome data.
  - `exposure_path`: The path to the exposure data.
  - `covariate_path`: The path to the covariate data.

These keys are used to generate a unique hash value for the project. One can add as many as keys as needed. The following is an example of a `project.yaml` file:

.. code-block:: yaml 
   name: cms_heart_failure
   id: 20221025
   details:
      description: Computing the effect of longterm pm2.5 exposure on lung cancer.
      version: 1.0.0
      authors:
         name: Naeem Khoshnevis 
         email: nkhoshnevis@g.harvard.edu
   data:
      outcome_path: project_abc/data/outcome.csv
      exposure_path: project_abc/data/exposure.csv
      covariate_path: project_abc/data/covariate.csv 

A note on the input data: The input data should have an `id` field that is the same for each observation in the outcome, exposure, and covariate data. All internal connections, and references are based on this `id` field. 

Now we can add the project to the database.

.. code-block:: python 
    >>> pc.create_project(folder_path = "project_abc")
    >>> pc.connect_to_project(folder_path = "project_abc")

A summary of pc will show the list of available projects.

.. code-block:: python
    >>> pc.summary()

Each project has an instance of main data node, which is generated during generating the project instance. Users can get that data node and start applying instructions.

.. code-block:: python
    >>> pr = pc.get_project(pr_name="cms_heart_failure")
    >>> mdn = pr.get_data_node()

Apply instructions
++++++++++++++++++

User can use any of the available instructions to apply to the data node. Here is the list of available instructions:
- filter: A plugin that is defined based on filtering mechanism in pandas dataframes.
- drop_na: A plugin that drops the rows that have missing values.

Instructions are defined as plugins each plugin has its own required fields and formats. Read more about plugins in :ref:`How to add plugins section <_how_to_add_plugins>`.

Let's say we want to apply the `filter` instruction to the data node. 

.. code-block:: python
   
    >>> instruction_1 = {"plugin_name": "filter", "filter_condition": "exposure > 2"}
    >>> mdn.apply(instruction_1)
    
This will create a new Data Node instance that is accessible from mdn object. The following code shows decsendants.

.. code-block:: python

    >>> mdn.descendants()
   
All objects, in the project has a unique hash value. The object is stored on the databases upon generating. Some internal commands that modify the object will also updates the object on the database. Each data object (DataNode instances) has all required information to reproduce that node. Original input data is not stored on the database, but the path to extract it is stored. More on this later. 

Now, let's say we know the hash value of the data node. We can extract it from database.

.. code-block:: python

    >>> n2 = pc.db.get_value("651f9f36ec80e919acbdaf740c3f8a026013c538073ce876ffd10a6cf6becab7")
    >>> n2.compute() 

`.compute()` method will compute the instructions on the data node and will store the results in the object.



