import json
from typing import Dict

from .types import ConsoleErrorField, UNKNOWN_CATEGORY_DESCRIPTION


def get_module(mod) -> Dict:
    mod_str = f"{mod:03}"
    try:
        with open(f"error-codes/{mod_str}/en_US.json") as f:
            error_json = json.load(f)
        module_json = error_json[mod_str]
        return module_json
    except FileNotFoundError:
        pass
    return None


def construct_support(ret, mod, desc):
    category = get_module(mod)

    # Bail early if category not found.
    if not category:
        ret.add_field(ConsoleErrorField('Category', supplementary_value=mod))
        ret.add_field(UNKNOWN_CATEGORY_DESCRIPTION)
        return ret

    ret.add_field(ConsoleErrorField('Category', message_str=category["name"], supplementary_value=mod))

    mod_str = f"{mod:03}"
    desc_str = f"{desc:04}"
    try:
        with open(f"error-codes/{mod_str}/{desc_str}/en_US.json") as f:
            error_json = json.load(f)
    except FileNotFoundError:
        pass

    description = error_json[mod_str][desc_str]

    # The descriptions in Pretendo's JSONs are kind of a mess.
    # Long descriptions and solutions often have "Unknown" on them, while short descriptions
    # have actual user-friendly dialogue.
    # So just use short descriptions, even though some error codes have quite detailed
    # long descriptions...
    ret.add_field(ConsoleErrorField('Description', message_str=description["short_description"]))
    ret.add_field(ConsoleErrorField('Solution', message_str=description["short_solution"]))
    ret.add_field(ConsoleErrorField('Further information', message_str=description["support_link"]))

    return ret
