"""Integrate commands in Nuke Nodes and Nuke menu."""

# import third-party modules
import nuke  # pylint: disable = import-error

# import local modules
from nuke_combine_grades import controller

nuke.menu('Nuke').addCommand("fhofmann/combine grades", controller.start, shortcut="f3")

