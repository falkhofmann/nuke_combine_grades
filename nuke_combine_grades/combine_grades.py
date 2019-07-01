
import nuke

COLOR_NODES = ['Add', 'Gamma', 'Grade', 'Multiply']

ADD_Order = ['value']
GAMMA_ORDER = ['value']
GRADE_ORDER = ['blackpoint', 'whitepoint', 'black', 'white', 'multiply', 'add', 'gamma']
MULTIPLY_ORDER = ['value']


def gather_possible_nodes(selected_node):

    current = selected_node

    nodes = [selected_node]
    while current.dependencies() and current.dependencies()[0].Class() in COLOR_NODES:
        current = current.dependencies()[0]
        nodes.append(current)
    return nodes


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
    start_node = nuke.selectedNode()
    if not start_node or start_node.Class() not in COLOR_NODES:
        return

    nodes = gather_possible_nodes(start_node)
    last_node = nodes[0]
    nodes.reverse()
    lut = set_up_colorlookup(last_node)

    channel_list = ['red', 'green', 'blue']
    for channel in channel_list:
        for step in frange(0.0, 1.0, 0.1):
            print float(step)
            lut['lut'].setValueAt(0.4, float(step), channel_list.index(channel) + 1)
