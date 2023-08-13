from sji_load_tables import get_joist_data

designation = '26K8'
span_ft = 44

joist = get_joist_data(designation,span_ft)
print(joist)

total_load = joist.total_load('ASD')
print(total_load)

total_load = joist.total_load('LRFD')
print(total_load)

total_load = joist.total_load('LRFD',units='kN/m')
print(total_load)

deflection_limit_load = joist.deflection_limit_load()
print(deflection_limit_load)

deflection_limit_load = joist.deflection_limit_load(units='kN/m')
print(deflection_limit_load)