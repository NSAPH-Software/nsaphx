nsaphx
======

.. image:: https://github.com/nsaph-software/nsaphx/workflows/Python\ package/badge.svg?branch=develop&event=push
    :target: https://github.com/nsaph-software/nsaphx/actions
    :alt: Test Status

*Causal Inference Studies*

nsaphx is a Python package designed for causal inference studies under the potential outcome framework. It provides a flexible and extensible framework for defining and applying computational instructions to input data, which should include outcome, exposure, and confounders. The package uses a directed acyclic graph and database storage to ensure efficient computation and storage of each object. Instruction handlers can be easily extended by defining new classes and methods, which can then be used to create new instructions that can be applied to data. Each object is computed only once and stored in the database, ensuring that computation is efficient and data is not duplicated.

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Introduction

   about

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Researchers

   setup_env
   quickstart
   faq

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Developers

   setup_env_dev
   documentation
   git_branching
   modules

.. toctree::
   :glob:
   :maxdepth: 2
   :caption: Community
   
   contact
   CHANGELOG.md






Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
