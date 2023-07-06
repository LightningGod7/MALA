import json
import os
from prettytable import PrettyTable


def beautify_menu(json_data):
    menu_data = json.loads(json_data)

    table = PrettyTable()
    table.field_names = ["Module Name", "Module Description", "Module Tagging"]
    table.max_table_width=120

    for item in menu_data:
        module = item["module"]
        description = item["description"]
        tagging = item["tagging"][0] if item["tagging"] else "None"

        table.add_row([module, description, tagging])

    return str(table)

with open('configs/modules.json', 'r') as file:
    json_data = file.read()
print(beautify_menu(json_data))
