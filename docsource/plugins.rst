Plugis
------

Plugins are a powerful way to extend the functionality of the application by defining instructions. These instructions can be applied to a data node, which contains data that comes from chains of previous instructions. Writing a plugin is an excellent way to contribute to the project, and the :ref:`how_to_add_plugins` section provides more details on how to do so.

Implemented plugins
+++++++++++++++++++

Instruction of all plugins should include `plugin_name` key. 

.. rst-class:: full-width

+---------------+-----------------------------------------+
| plugin name   | plugin required fields                  | 
+===============+=========================================+
| `filter`      | `plugin_name`, `filter_condition`       |
+---------------+-----------------------------------------+
| `drop_na`     | `plugin_name`                           |
+---------------+-----------------------------------------+

filter
~~~~~~

The filter plugin allows the user to filter the data based on a set of rules. Internally it uses the `query` function in the `pandas` library.

This plugin conducts the following steps:

- Load data from the database and join them based on the id column.
- Apply the `filter_condition` as a query to the data.
- Select the `id` column from the filtered data.
- Generate `output_data` dictionary and assign the selected ids to `d_index` field.
- Return the `output_data` dictionary.

See the :ref:`data_node` section for more details on `d_index`.

Here are a couple of examples:

.. code-block:: python

     >>> instruction_1 = {"plugin_name": "filter", "filter_condition": "exposure > 10"}
     >>> instruction_2 = {"plugin_name": "filter", "filter_condition": "cs_white > 0.45 & cs_white < 0.8"}
     >>> instruction_3 = {"plugin_name": "filter", "filter_condition": "cs_household_income > 15000"}

drop_na
~~~~~~~

This is similar to the `filter` plugin. The only difference is that it drops rows that contain `NaN` values. 

This plugin conducts the following steps:

- Load data from the database and join them based on the id column.
- Drop rows with missing values.
- Select the `id` column from the remaining data.
- Generate `output_data` dictionary and assign the selected ids to `d_index` field.
- Return the `output_data` dictionary.

Here is an example:

.. code-block:: python

     >>> instruction_4 = {"plugin_name": "drop_na"}


