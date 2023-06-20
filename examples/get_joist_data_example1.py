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

live_load = joist.live_load()
print(live_load)

live_load = joist.live_load(units='kN/m')
print(live_load)