from unittest import TestCase

from cwlpy import WorkflowStep, WorkflowStepInput, WorkflowStepOutput, ValidationException


class WorkflowStepTestCase(TestCase):

    def setUp(self):
        self.step = WorkflowStep('my-step')

    def test_id(self):
        self.assertEqual(self.step.id, 'my-step')

    def test_save(self):
        saved = self.step.save()
        self.assertEqual(saved['id'], 'my-step')

    def test_add_input(self):
        step_input = WorkflowStepInput('step-input-1')
        self.step.add_input(step_input)
        self.assertIn(step_input, self.step.in_)

    def test_validates_add_input_type(self):
        with self.assertRaises(ValidationException) as cm:
            self.step.add_input('a string')
        self.assertIn('Not a WorkflowStepInput', repr(cm.exception))

    def test_validates_add_input_uniqueness(self):
        self.step.add_input(WorkflowStepInput('step-input-1'))
        with self.assertRaises(ValidationException) as cm:
            self.step.add_input(WorkflowStepInput('step-input-1'))
        self.assertIn('Step already has input with id', repr(cm.exception))

    def test_add_output(self):
        step_output = WorkflowStepOutput('step-output-1')
        self.step.add_output(step_output)
        self.assertIn(step_output, self.step.out)

    def test_validates_add_output_type(self):
        with self.assertRaises(ValidationException) as cm:
            self.step.add_output('a string')
        self.assertIn('Not a WorkflowStepOutput', repr(cm.exception))

    def test_validates_add_output_uniqueness(self):
        self.step.add_output(WorkflowStepOutput('step-output-1'))
        with self.assertRaises(ValidationException) as cm:
            self.step.add_output(WorkflowStepOutput('step-output-1'))
        self.assertIn('Step already has output with id', repr(cm.exception))

    def test_validates_set_run(self):
        # Must be one of six.string_types, CommandLineTool, ExpressionTool, Workflow]
        with self.assertRaises(ValidationException) as cm:
            self.step.set_run(1000)
        self.assertIn('Not an allowed type', repr(cm.exception))

    def test_set_run(self):
        self.step.set_run('tool.cwl')
        self.assertEqual(self.step.run, 'tool.cwl')

    def test_finds_workflow_step_output_by_id(self):
        step_output = WorkflowStepOutput('step-output-1')
        self.step.add_output(step_output)
        self.assertEqual(self.step.workflow_step_output_by_id('step-output-1'), step_output)
        self.assertIsNone(self.step.workflow_step_output_by_id('foobar'))
