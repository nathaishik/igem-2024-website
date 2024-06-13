from django.test import TestCase
from notebook.models import *
from django.db.utils import IntegrityError

# Testing data
class NotebookTestCaseModels(TestCase):
    def setUp(self):

        # Create users
        u1 = User.objects.create_user(username="user1", password="password1")
        u1.verified = True
        u1.position = 1
        u1.save()
        User.objects.create_user(username="user2", password="password2")

        # Create departments
        d1 = Department.objects.create(name="Department 1", code="DEPMT1")
        d2 = Department.objects.create(name="Department 2", code="DEPMT2")

        # Create notes
        Note.objects.create(user=u1, published=True, title="Note 1", department=d1, content="Content 1")
        Note.objects.create(user=u1, title="Note 2", department=d2, content="Content 2")
        Note.objects.create(user=u1, title="Note 6", department=d1, content="Content 6")

    def test_invalid_user(self):
        """User should not be created as the username is not unique."""
        with self.assertRaises(IntegrityError) as context:
            User.objects.create(username="user1", password="password3") # should be invalid as username is not unique
        self.assertTrue('UNIQUE constraint failed' in str(context.exception))
    
    def test_invalid_department(self):
        """Department 3 should not be created as the code is not unique."""
        with self.assertRaises(IntegrityError) as context:
            Department.objects.create(name="Department 3", code="DEPMT1") # should be invalid as code is not unique
        self.assertTrue('UNIQUE constraint failed' in str(context.exception))

    def test_invalid_department_note(self):
        """Note 3 should not be created as the department does not exist."""
        with self.assertRaises(Department.DoesNotExist) as context:
            Note.objects.create(user=User.objects.get(username="user1"), title="Note 3", department=Department.objects.get(name="Department 3"), content="Content 3")
        self.assertTrue('Department matching query does not exist.' in str(context.exception))

    def test_unverified_user_note_db(self):
        """Note 3 should be created even though the user is not verified as this is from the admin side."""
        u2 = User.objects.get(username="user2")
        Note.objects.create(user=u2, title="Note 3", department=Department.objects.get(name="Department 1"), content="Content 3")
        self.assertEqual(u2.notes.all().count(), 1)

    def test_non_user_note(self):
        """Note 4 should not be created as the user does not exist."""
        with self.assertRaises(User.DoesNotExist) as context:
            Note.objects.create(user=User.objects.get(username="user3"), title="Note 4", department=Department.objects.get(name="Department 1"), content="Content 4")
        self.assertTrue('User matching query does not exist.' in str(context.exception))
    
    def test_user_count(self):
        """There should be only 2 users."""
        self.assertEqual(User.objects.all().count(), 2)
    
    def test_department_count(self):
        """There should be only 2 departments. d3 does not have unique code and names and should not exist."""
        self.assertEqual(Department.objects.all().count(), 2)

    def test_note_count(self):
        """There should be only 3 notes. n3, n4, and n5 should not exist."""
        self.assertEqual(Note.objects.all().count(), 3)
    
    def test_note_published(self):
        """There should be only 1 published note."""
        self.assertEqual(Note.objects.filter(published=True).count(), 1)

    def test_note_proper_user(self):
        """u1 should have 3 notes"""
        u1 = User.objects.get(username="user1")
        self.assertEqual(u1.notes.all().count(), 3)

    def test_department_note_count(self):
        """d1 should have 2 notes"""
        d1 = Department.objects.get(name="Department 1")
        self.assertEqual(d1.notes.all().count(), 2)

    # Testing file uploads
    def test_file_upload(self):
        """File should be uploaded to the correct path and should be correctly changed"""
        n = Note.objects.get(title="Note 1")
        with open("notebook/test_files/test.txt", "rb") as f1:
            n.file = f1
            self.assertEqual(f1, n.file)
        with open("notebook/test_files/test1.txt", "rb") as f2:
            n.file = f2
            self.assertEqual(f2, n.file)

