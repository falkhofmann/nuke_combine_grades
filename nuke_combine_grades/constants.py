
# Import local modules
from nuke_combine_grades import nodes

reload(nodes)

KNOBS = {'Add': ['value'],
         'Gamma': ['value'],
         'Grade': ['blackpoint', 'whitepoint', 'black', 'white', 'multiply', 'add', 'gamma'],
         'Multiply': ['value']}

COLOR_NODES = ['Add', 'Gamma', 'Grade', 'Multiply']

NODE_MAP = {'Add': nodes.Add,
            'Gamma': nodes.Gamma,
            'Grade': nodes.Grade,
            'Multiply': nodes.Multiply}
