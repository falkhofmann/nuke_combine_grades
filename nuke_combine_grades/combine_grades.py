
import nuke


import nodes
import utils

reload(nodes)
COLOR_NODES = ['Add', 'Gamma', 'Grade', 'Multiply']

NODE_MAP = {'Add': nodes.Add,
            'Gamma': nodes.Gamma,
            'Grade': nodes.Grade,
            'Multiply': nodes.Multiply}


def frange(start, stop=None, step=None):

    if stop is None:
        stop = start + 0.0
        start = 0.0
    if step is None:
        step = 1.0
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
    return look_up


def start():
    nodes = nuke.selectedNodes()
    # if not all([node.Class() in COLOR_NODES for node in nodes]):
    #     return


    lut = set_up_colorlookup(nodes[0])

    y_min = 0.0
    y_max = 5.0
    x_steps = 10

    karl = (y_max-y_min)/float(x_steps)

    for step in frange(y_min, y_max + karl, karl):
        step = float(step)
        for node in nodes:
            args = [step] + utils.prep_args(node)
            calc = NODE_MAP[node.Class()](*args)
            for idx, value in enumerate(calc.values_out):
                lut['lut'].setValueAt(value, step, idx + 1)
