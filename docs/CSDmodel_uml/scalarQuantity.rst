
.. _sQ_uml:

--------------
ScalarQuantity
--------------

ScalarQuantity is an object composed of a numerical value and any valid SI unit
symbol or any number of accepted non-SI unit symbols. It is serialized in the
JSON file as a string containing a numerical value followed by the unit symbol,
for example,

- "3.4 m" (SI)
- "2.3 bar" (non-SI)
