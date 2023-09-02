
# sji_load_tables

*A **Python Library** for looking up values from the Steel Joist Institute (SJI) load tables​*

Developed and maintained by **Mark Denavit's** research group, authorized by the Steel Joist Institute.

The load table data is based on the [44th Edition Catalog](https://steeljoist.org/product/44th-edition-standard-specifications-load-tables-and-weight-tables-for-steel-joists-and-joist-girders-2-2/).

This Python library is for general information only. It is intended to be an accurate, reliable, and 
useful tool, however, it should not be used or relied upon for any specific project without competent 
professional assessment of its accuracy, suitability, and applicability. Any person using this Python 
library does so at their own risk and assumes all liability arising from such use.

Please report any bugs, errors, feature requests to [Prof. Denavit](https://cee.utk.edu/people/mark-denavit/) 
or [create an issue](https://github.com/denavit/sji_load_tables/issues/new/choose).

## Install

```sh
pip install sji_load_tables
```

## Example Usage

### Data Lookup
```
>>> import sji_load_tables as sji
>>> joist = sji.get_joist_data('26K8',44) # 26K8 joist with a span of 44 ft
>>> print(joist.total_load('ASD')) # default output units are lbs/ft
251.0
>>> print(joist.total_load('LRFD'))
376.0
>>> print(joist.total_load('LRFD',units='kN/m'))
5.49
>>> print(joist.deflection_limit_load())
143.0
```

### Find Lightest Joist
```
>>> import sji_load_tables as sji
>>> # Find the lightest K series joist with a span of 45 ft and total load of 250 lbs/ft ASD
>>> joist = sji.lightest_joist(45,250,design_basis='ASD',series='K')
>>> print(joist)
30K7 joist, span_ft=45, approx_wt_plf=9.6
  total_load_ASD_plf=251.0, deflection_limit_load_plf=164.0
  erection_bridging_color_code=Red
```
 
[License]: LICENSE



