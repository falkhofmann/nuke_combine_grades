"""Controller to connect model with view."""

# Import third-party module
import nuke

# Import local modules
from nuke_combine_grades import constants
from nuke_combine_grades import model
from nuke_combine_grades import utils
from nuke_combine_grades import view


def start():
    """Start up function."""
    nodes = utils.start_up_check()
    if not nodes:
        nuke.message('Please check your selection.\n'
                     'Allowed nodes are:\n\n{}'.format('\n'.join(constants.COLOR_NODES)))
        return
    panel = view.CombineGradePanel()
    dialog = panel.showModalDialog()
    if not dialog:
        return
    model.combine_grades(nodes,
                         panel.minimim.value(),
                         panel.maximum.value(),
                         panel.steps.value())
