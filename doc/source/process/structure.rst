Process structure
=================
In the file, containing the process, there must be one class, with the name
:class:`Process`, which is instance of :class:`pywps.Process.WPSProcess` class.
Each process must contain at least two methods:
:meth:`pywps.Process.WPSProcess.__init__` and :meth:`pywps.Process.WPSProcess.execute` .

.. _process-initialization:
Process initialization: __init__ method
---------------------------------------
This method is constructor for the actual process. It has to invoke :meth:`pywps.Process.WPSProcess.__init__` method of the superior `WPSProcess` class with process configuration options, described in :class:`pywps.Process.WPSProcess` more detaily.


The process can than define several
:class:`pywps.Process.InAndOutputs.Input` and
:class:`pywps.Process.InAndOutputs.Output` . Several methods can be used
for this, namely :meth:`pywps.Process.WPSProcess.addLiteralInput`, :meth:`pywps.Process.WPSProcess.addComplexInput`, :meth:`pywps.Process.WPSProcess.addBBoxInput` for inputs and  :meth:`pywps.Process.WPSProcess.addLiteralOutput`, :meth:`pywps.Process.WPSProcess.addComplexOutput`, :meth:`pywps.Process.WPSProcess.addBBoxOutput` for outputs.

Process execution: execute method
---------------------------------
The :meth:`pywps.Process.WPSProcess.execute` method, which is originally
empty, is the one, which is called by PyWPS, when it comes to process
execution. The actual calculation is to be done here. When the process
returns any text, it is handled as error message. Processes is successfully
calculated, when this method returns None.

Example of PyWPS process 
------------------------

.. literalinclude:: ../../../examples/returner.py
   :language: python

After adding `"returner"` string to `__all__` array, in the
:file:`__init__.py`  file in the PyWPS Processes directory, we can try
GetCapabilities, DescribeProcess and Execute requests.
