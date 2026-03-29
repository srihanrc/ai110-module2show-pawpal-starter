"""
Test cases for PawPal pet care system
"""

import unittest
from pawpal_system import Task, Pet


class TestPawPal(unittest.TestCase):
    """Test cases for PawPal system components"""

    def test_task_completion(self):
        """Test that calling mark_completed() changes the task's status"""
        # Create a task
        task = Task("Test task", 30, "Daily")

        # Initially, task should be incomplete
        self.assertFalse(task.is_completed, "Task should start as incomplete")

        # Mark as completed
        task.mark_completed()

        # Verify task is now completed
        self.assertTrue(task.is_completed, "Task should be completed after mark_completed()")

        # Mark as incomplete again
        task.mark_incomplete()

        # Verify task is back to incomplete
        self.assertFalse(task.is_completed, "Task should be incomplete after mark_incomplete()")

    def test_task_addition_to_pet(self):
        """Test that adding a task to a Pet increases that pet's task count"""
        # Create a pet
        pet = Pet("TestPet", "Dog", "Kibble", [])

        # Initially, pet should have no tasks
        initial_count = len(pet.get_tasks())
        self.assertEqual(initial_count, 0, "Pet should start with no tasks")

        # Create and add a task
        task = Task("Test task", 30, "Daily")
        pet.add_task(task)

        # Verify task count increased
        new_count = len(pet.get_tasks())
        self.assertEqual(new_count, 1, "Pet should have 1 task after adding")

        # Verify the task is in the pet's task list
        self.assertIn(task, pet.get_tasks(), "Added task should be in pet's task list")

        # Verify the task is associated with the pet
        self.assertEqual(task.get_pet(), pet, "Task should be associated with the pet")


