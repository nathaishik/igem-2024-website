from django.test import TestCase, Client
from django.urls import reverse
from notebook.models import *

class NotebookTestCaseViews(TestCase):
    def setUp(self):

        # Create users
        u1 = User.objects.create_user(username="user1", password="password1")
        u1.verified = True
        u1.position = "STUDENT"
        u1.save()
        User.objects.create_user(username="user2", password="password2")

        # Create departments
        d1 = Department.objects.create(name="Department 1", code="DEPMT1")
        d2 = Department.objects.create(name="Department 2", code="DEPMT2")

        # Create notes
        Note.objects.create(user=u1, published=True, title="Note 1", department=d1, content="Content 1")
        Note.objects.create(user=u1, title="Note 2", department=d2, content="Content 2")
        Note.objects.create(user=u1, title="Note 6", department=d1, content="Content 6")

    # Testing the website

    def test_homepage(self):
        """This should return a 404 error as there is no homepage."""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 404)

    def test_valid_indexpage(self):
        """This should return a 200 status code. Then the number of departments should be 2 and the title content should be None."""
        c = Client()
        response = c.get(reverse('notebook:index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context.get("title"), None)
        self.assertEqual(response.context["departments"].count(), 2)
        
    def test_valid_notebook(self):
        """This should return a 200 status code. Then the number of notes should be 1 and the notebook context should be Department 1."""
        c = Client()
        response = c.get(reverse('notebook:notebook', args=["DEPMT1"]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notebook"], "Department 1")
        self.assertEqual(response.context["notes"].count(), 1)
        self.assertEqual(response.context["notes"][0].title, "Note 1")
    
    def test_invalid_notebook(self):
        """This should return a 404 error as the department should not exist."""
        c = Client()
        response = c.get(reverse('notebook:notebook', args=["DEPMT3"]))
        self.assertEqual(response.status_code, 404)

    def test_login_page(self):
        """This should return a 200 status code."""
        c = Client()
        response = c.get(reverse('notebook:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login(self):
        """This should return a 200 status code and user should be logged in"""
        c = Client()
        response = c.post(reverse('notebook:login'), {"username": "user1", "password": "password1"})
        self.assertEqual(response.status_code, 302)

    def test_invalid_login(self):
        """This should return a 200 status code and the message of Invalid username and/or password."""
        c = Client()
        response = c.post(reverse('notebook:login'), {"username": "user1", "password": "password2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Invalid credentials")
    
    def test_register_page(self):
        """This should return a 200 status code."""
        c = Client()
        response = c.get(reverse('notebook:register'))
        self.assertEqual(response.status_code, 200)

    def test_valid_register(self):
        """This should return a 200 status code and three users should be created"""
        c = Client()
        response = c.post(reverse('notebook:register'), {"username": "user4", "password": "password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "password4"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 3)

    def test_invalid_password_register(self):
        """This should return a 200 status code and the message of Passwords must match."""
        c = Client()
        response = c.post(reverse('notebook:register'), {"username": "user4", "password": "password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "password5"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Passwords must match")

    def test_invalid_username_register(self):
        """This should return a 200 status code and the the message of Invalid username."""
        c = Client()
        response = c.post(reverse('notebook:register'), {"username": "user1", "password": "password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "password4"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Invalid username")

    def test_unloggedin_dashboard(self):
        """Since the user is not logged in, this should redirect to the login page."""
        c = Client()
        response = c.get(reverse('notebook:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '../login?next=/docs/dashboard/')

    def test_loggedin_dashboard(self):
        """Since the user is logged in, this should return a 200 status code and 3 note objects."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"].all().count(), 3)

    def test_logout(self):
        """This should return a 302 status code and redirect to the index page."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notebook:index'))

    def test_upload_page(self):
        """This should return a 200 status code."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:upload'))
        self.assertEqual(response.status_code, 200)

    def test_new_note(self):
        """This should return a 302 status code and redirect to the dashboard and confirm the correct number of notes: 4"""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:upload'), {"title": "Note 7", "department": 1, "content": "Content 7"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.all().count(), 4)

    def test_unverified_user_note_client(self):
        """This should return a 302 status code and redirect to the dashboard and confirm the correct number of notes: 3"""
        c = Client()
        c.login(username="user2", password="password2")
        response = c.post(reverse('notebook:upload'), {"title": "Note 5", "department": "1", "content": "Content 5"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notebook:dashboard'))
        self.assertEqual(Note.objects.all().count(), 3)
    
    def test_invalid_new_note(self):
        """This should return a 200 status code due to invalid department."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:upload'), {"title": "Note 8", "department": 3, "content": "Content 8"})
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.context["message"], "Something went wrong. Please try again.")
        self.assertEqual(Note.objects.all().count(), 3)

    def test_manage_note_page(self):
        """This should return a 200 status code."""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        response = c.get(reverse('notebook:manage_note'), {"edit": u.notes.all()[0].id})
        self.assertEqual(response.status_code, 200)

    def test_edited_note(self):
        """This should return a 200 status code and redirect to the note and confirm the correct number of notes: 3"""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        response = c.post(reverse('notebook:manage_note'), {"edit": u.notes.all()[0].id, "title": "Note 1", "department": "1", "content": "Content 1 edited", "published": True}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.all().count(), 3)
        self.assertEqual(u.notes.all()[0].content, 'Content 1 edited')
    
    def test_invalid_edit_note(self):
        """This should return a 200 status code and the message of Something went wrong. Please try again."""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        response = c.post(reverse('notebook:manage_note'), {"edit": u.notes.all()[0].id, "title": "Note 1", "department": "3", "content": "Content 1 edited", "published": True})
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.context["message"], "Something went wrong. Please try again.")
        self.assertEqual(u.notes.all()[0].content, 'Content 1')
        

