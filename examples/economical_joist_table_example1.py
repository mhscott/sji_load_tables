from sji_load_tables import economical_joist_table

span = 40

joists = economical_joist_table(span,series='K')

joists = economical_joist_table(span,series='K',load_type='Deflection Limit Load')
