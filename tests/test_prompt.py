import json
from utils import load_json_from_file

def load_test_workflow():
    workflow = load_json_from_file('workflow.json')
    return workflow