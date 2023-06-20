import importlib.resources
import json

try:
    f = importlib.resources.read_text("sji_load_tables.data", "joist_data.json")
    save_object = json.loads(f)
    joist_database = save_object['joist_database']
    joists_sorted_by_weight = save_object['joists_sorted_by_weight']
    del f, save_object
except:
    import warnings
    warnings.warn('joist_database did not load, setting to empty dict')
    joist_database = dict()
    joists_sorted_by_weight = []