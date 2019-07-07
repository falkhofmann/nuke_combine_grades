
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


def set_up_colorlookup(last_node):
    """Create and set up ColorLookup node to use RGBA.

    Returns:
        nuke.node: New created node.

    """
    look_up = nuke.nodes.ColorLookup(xpos=last_node.xpos(),
                                     ypos=last_node.ypos()+100)
    look_up.setLabel('Combined color operations.')
    for channel in range(1, 5):
        look_up['lut'].removeKeyAt(0.0, channel)
        look_up['lut'].removeKeyAt(1.0, channel)
    return look_up


def combine_grades(user_nodes, minimum, maximum, steps):

    lut = set_up_colorlookup(user_nodes[0])
    if minimum == 0:
        minimum = 0.0000001

    step = (maximum-minimum)/float(steps)

    user_nodes.reverse()
    range_ = list(frange(minimum, maximum, step))
    if 1.0 not in range_:
        range_.append(float(1.0))
    for each_step in range_:
        each_step = [float(each_step) for _ in range(4)]
        current_color = each_step
        for node in user_nodes:

            args = [current_color] + utils.prep_args(node)
            calc = constants.NODE_MAP[node.Class()](*args)
            current_color = calc.values_out

        for idx, value in enumerate(calc.values_out):
            lut['lut'].setValueAt(value, each_step[idx], idx + 1)
