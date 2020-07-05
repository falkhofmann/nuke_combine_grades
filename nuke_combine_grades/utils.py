"""Util functions to use across package."""

# Import third-party module
import nuke

# Import local modules
from nuke_combine_grades import constants


def prep_args(node):
    """Prepare arguments work with nodes classes.

    Args:
        node (nuke.Node):  Node to get knob data from.

    Returns:
        list: All relevant knob data for baking.

    """
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
    """Verify if selected nodes are valid node classes."""
    nodes = nuke.selectedNodes()
    if not all([node.Class() in constants.COLOR_NODES for node in nodes]):
        return
    else:
        return nodes
