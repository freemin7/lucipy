.. _lucipy-detection:

Endpoints and Autodetection
===========================

*LUCIDAC Endpoints* are URL-like notations for addressing the connection to a
LUCIDAC device. The concept is described in the
`Firmware docs <https://anabrid.dev/docs/hybrid-controller/>`_ and is similar to
the `NI VISA resource syntax <https://www.ni.com/docs/en-US/bundle/ni-visa/page/visa-resource-syntax-and-examples.html>`_

Which endpoint notation and protocol support is available depends on the client
implementation. Lucipy understands the following endpoints:

* ``serial:/`` - USB Serial terminals speaking JSONL
* ``tcp:/`` - "Raw" TCP/IP speaking JSONL
* ``sim:/`` - A shorthand to the integrated simulator

For convenience, the :ref:`client code <lucipy-client>` allows for autodetection
of the endpoint using MDNS/Zeroconf. This works by making an instance without
providing the endpoint:

::

   >>> from lucipy import LUCIDAC
   >>> hc = LUCIDAC() # this will trigger the autodetection

Direct access to the underlying API should not be neccessary, but is possible
with :code:`import lucipy.detect`. The following reference shows the exposed
functions.

.. note::

   *lucipy* does not have explicit dependencies by design.
   Autodetection functionality requires these relevant libraries: 
   `zeroconf <https://python-zeroconf.readthedocs.io/>`_ and/or
   `pySerial <https://pyserial.readthedocs.io/>`_ .
   
   If these dependencies are not installed, the code will throw errors suggesting
   you to install them in order to make autodetection work. In this case
   :code:`hc = LUCIDAC()` will not work and an endpoint argument is required instead.
   

Code refererence
----------------

.. automodule:: lucipy.detect
   :members:
