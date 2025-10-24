import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.utils import csv_to_json

# Convert local authority names from csv files to json
csv_to_json(
    'data/reference/commissioning_bodies.csv', 
    'commissioning_body', 
    'data/reference', 
    'commissioning_bodies.json'
    )