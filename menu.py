"""Integrate commands in Nuke Nodes and Nuke menu."""

# import third-party modules
import nuke  # pylint: disable = import-error

# import local modules
from nuke_combine_grades import controller


def dev_2():
    reload(controller)
    controller.start()


nuke.menu('Nuke').addCommand("fhofmann/combine grades", dev_2, shortcut="f3")

