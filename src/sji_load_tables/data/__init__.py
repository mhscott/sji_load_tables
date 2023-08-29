import importlib.resources
import json
import sys

if sys.version_info < (3, 9):
    _read_text = importlib.resources.read_text
else:
    def _read_text(package, resource):
        return importlib.resources.files(package).joinpath(resource).read_text()


def load_data():
    f = _read_text(__package__, 'joist_data.json')
    save_object = json.loads(f)
    joist_database = save_object['joist_database']
    joists_sorted_by_weight = save_object['joists_sorted_by_weight']
    return joist_database, joists_sorted_by_weight


try:
    joist_database, joists_sorted_by_weight = load_data()
except Exception as exc:
    raise RuntimeError("Failed to load joist database") from exc