
# Import third-party module
import nuke

# Import local modules
from nuke_combine_grades import constants

reload(constants)


def prep_args(node):
    all_values = []

    for knob in constants.KNOBS[node.Class()]:
        values = node[knob].value()

        if isinstance(values, float):
            knob_values = [values for _ in range(4)]
        else:
            knob_values = values

        all_values.append(knob_values)
    all_values.append(node['mix'].value())
    return all_values


def start_up_check():
    nodes = nuke.selectedNodes()
    if not all([node.Class() in constants.COLOR_NODES for node in nodes]):
        return
    else:
        return nodes
