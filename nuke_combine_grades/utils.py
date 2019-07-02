KNOBS = {'Add': ['value'],
         'Gamma': ['value'],
         'Grade': ['blackpoint', 'whitepoint', 'black', 'white', 'multiply', 'add', 'gamma'],
         'Multiply': ['value']}


def prep_args(node):
    knob_values = []
    all_values = []

    for knob in KNOBS[node.Class()]:
        if len(knob) == 1:
            knob_values = [node[knob].value() for _ in range(3)]
        else:
            knob_values = node[knob].value()
    all_values.append(knob_values)
    all_values.append(node['mix'].value())
    return all_values
