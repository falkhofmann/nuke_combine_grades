"""Define constants values to use across package."""

# Import local modules
from nuke_combine_grades import nodes

# Knob definition per color node.
KNOBS = {'Add': ['value'],
         'Gamma': ['value'],
         'Grade': ['blackpoint', 'whitepoint', 'black', 'white', 'multiply', 'add', 'gamma'],
         'Multiply': ['value']}

# Allowed nodes to bake.
COLOR_NODES = KNOBS.keys()

# Map noe class to to nukes built in command.
NODE_MAP = {'Add': nodes.Add,
            'Gamma': nodes.Gamma,
            'Grade': nodes.Grade,
            'Multiply': nodes.Multiply}
