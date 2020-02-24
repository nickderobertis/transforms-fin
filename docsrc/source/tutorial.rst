Getting started with transforms_fin
**********************************

Install
=======

Install via::

    pip install transforms_fin

Usage
=========

Some highlighted functionality.

This is a simple example::

    import transforms_fin  # transforms are automatically loaded upon import
    import datacode as dc

    a = dc.Variable('a', 'A')
    vc = dc.VariableCollection(a)

    # Portfolio transform
    vc.a.port()


