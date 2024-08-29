.. _intro:

Introduction
============


``lucipy`` is a Python3 package and low boilerplate and easy to follow code allowing users
to get started with the `LUCIDAC <https://anabrid.com/luci>`_
analog-digital hybrid computer. With this library, users can program the
network-enabled analog computer easily and using the Python programming language.
Lucipy empowers users to integrate analog computers as solvers into their
favourite scientific python environment. It is convenient to use in interactive 
environments such as IPython or Jupyter. For other use cases the ``pybrid`` code might be
preferred. See :ref:`comparison` for details.

Lucipy is still in active development and currently provides

* the simple hybrid controller class :py:class:`.LUCIDAC`
* basic syntactic sugar for route-based analog circuit programming with :py:class:`.Circuit`
* various example applications (basically the
  `analog paradigm application notes <https://analogparadigm.com/documentation.html>`_)
* tools like an Over-The-Air firmware updater
* routines for device autodiscovery with zeroconf and USB Serial detection

The code was formerly known as "Synchronous Hybrid Controller Python Client for REDAC/LUCIDAC"
(shcpy) and was primarily used for testing protocol extensions and new firmware features.
