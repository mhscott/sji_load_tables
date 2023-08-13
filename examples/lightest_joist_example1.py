from sji_load_tables import lightest_joist

span = 45
required_total_load = 250
required_deflection_limit_load = 50 # e.g., live load

joist = lightest_joist(span,required_total_load,required_deflection_limit_load,design_basis='ASD',series='K')
print(joist)

joist = lightest_joist(span,required_total_load,required_deflection_limit_load,design_basis='ASD',series='K',no_erection_bridging=True)
print(joist)