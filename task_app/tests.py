from django.test import TestCase

# Create your tests here.

from task_app.models import Task


class TaskTests(TestCase):
    """Task model tests."""

    def test_str(self):
        task = Task(title='Title', description='Desc')
        self.assertEquals(
            str(task),
            'Title Desc',
        )
