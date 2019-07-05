import nuke
import nukescripts


class CombineGradePanel(nukescripts.PythonPanel):

    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'hans')

        self.range_text = nuke.Text_Knob('range_text', 'define range to rasterize')
        self.minimim = nuke.Int_Knob('minimum')
        self.maximum = nuke.Int_Knob('maximum')

        self.step_text = nuke.Text_Knob('step_text', 'define steps to rasterzie')
        self.steps = nuke.Int_Knob('steps')

        self.minimim.setValue(0)
        self.maximum.setValue(1)
        self.steps.setValue(10)

        for knob in (self.range_text, self.minimim, self.maximum, self.step_text, self.steps):
            self.addKnob(knob)

        nukescripts.PythonPanel._makeOkCancelButton(self)
