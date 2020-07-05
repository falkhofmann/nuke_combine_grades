# Import third-party module
import nuke

# Import local modules
from nuke_combine_grades import constants
from nuke_combine_grades import nodes
from nuke_combine_grades import utils

reload(constants)
reload(nodes)
reload(utils)


def frange(start, stop, step):
    while True:
        if step > 0 and start >= stop:
            break
        elif step < 0 and start <= stop:
            break
        yield ("%g" % start)
        start = start + step


def find_upstream_nodes(color_nodes, nd_input):
    for i_input_idx in range(nd_input.inputs()):
        if nd_input.input(i_input_idx).Class() in constants.COLOR_NODES:
            color_nodes.append(nd_input.input(i_input_idx))
        find_upstream_nodes(color_nodes, nd_input.input(i_input_idx))


def set_up_colorlookup(top_color_node):
    """Create and set up ColorLookup node to use RGBA.

    Returns:
        nuke.node: New created node.

    """

    node_above_color_nodes = top_color_node.dependencies(nuke.INPUTS|nuke.HIDDEN_INPUTS)
    if node_above_color_nodes:
        top_color_node = node_above_color_nodes[0]

    look_up = nuke.nodes.ColorLookup(xpos=top_color_node.xpos() + 150,
                                     ypos=top_color_node.ypos(),
                                     tile_color=3126067455,
                                     inputs=[top_color_node])

    for channel in range(1, 5):
        look_up.knob("lut").removeKeyAt(0.0, channel)
        look_up.knob("lut").removeKeyAt(1.0, channel)

    look_up.knob("label").setValue('Combined color operations.')

    return look_up


def combine_grades(user_nodes, minimum, maximum, steps):

    node = user_nodes[0]
    color_nodes = list()
    if node.Class() in constants.COLOR_NODES:
        color_nodes.append(node)
    find_upstream_nodes(color_nodes, node)

    lut = set_up_colorlookup(color_nodes[-1])
    if minimum == 0:
        minimum = 0.0000001

    step = (maximum - minimum) / float(steps)

    color_nodes.reverse()
    range_ = list(frange(minimum, maximum, step))
    if 1.0 not in range_:
        range_.append(float(1.0))
    for each_step in range_:
        each_step = [float(each_step) for _ in range(4)]
        current_color = each_step
        for node in color_nodes:
            args = [current_color] + utils.prep_args(node)
            calc = constants.NODE_MAP[node.Class()](*args)
            current_color = calc.values_out

        for idx, value in enumerate(calc.values_out):
            lut['lut'].setValueAt(value, each_step[idx], idx + 1)
