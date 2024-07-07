from django.test import TestCase, Client
from django.urls import reverse
from notebook.models import *
import filecmp
import json
import uuid

class NotebookTestCaseViews(TestCase):
    def setUp(self):

        # Create users
        u1 = User.objects.create_user(username="user1", password="password1")
        u1.save()
        u2 = User.objects.create_user(username="user2", password="password2")
        u2.position = 2
        u2.save()
        u3 = User.objects.create_user(username="user3", password="password3")
        u3.save()

        # Create departments
        d1 = Department.objects.create(name="Department 1", code="DEPMT1")
        d2 = Department.objects.create(name="Department 2", code="DEPMT2")

        d1.members.add(u1)
        d1.members.add(u3)
        d2.leader.add(u1)
        d2.members.add(u1)
        d2.members.add(u2)
        d2.waitlist.add(u3)
        
        # Create notes
        Note.objects.create(user=u1, published=True, title="Note 1", department=d1, content="Content 1")
        Note.objects.create(user=u1, title="Note 2", department=d2, content="Content 2")
        Note.objects.create(user=u1, title="Note 6", department=d1, content="Content 6")

    # Testing the views

    def test_homepage(self):
        """This should load the index page with status code 200"""
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)

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
        response = c.post(reverse('notebook:register'), {"username": "user4", "password": "long_enough_password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "long_enough_password4"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 4)

    def test_invalid_password_register(self):
        """This should return a 200 status code and the message of Passwords must match."""
        c = Client()
        response = c.post(reverse('notebook:register'), {"username": "user4", "password": "password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "password5"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Passwords must match")

    def test_invalid_username_register(self):
        """This should return a 200 status code and the the message of Invalid username."""
        c = Client()
        response = c.post(reverse('notebook:register'), {"username": "user1", "password": "long_enough_password4", "email": "user4@mail.com", "first": "User", "last": "Four", "confirmation": "long_enough_password4"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["message"], "Invalid username")

    def test_unloggedin_dashboard(self):
        """Since the user is not logged in, this should redirect to the login page."""
        c = Client()
        response = c.get(reverse('notebook:dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'..{reverse("notebook:login")[0:-1]}?next={reverse("notebook:dashboard")}')

    def test_loggedin_dashboard(self):
        """Since the user is logged in, this should return a 200 status code and 1 published and 2 draft note objects."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"].all().count(), 1)
        response = c.get(reverse('notebook:dashboard')+'?filter=drafts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["notes"].all().count(), 2)

    def test_logout(self):
        """This should return a 302 status code and redirect to the index page."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notebook:login'))

    def test_upload_page(self):
        """This should return a 200 status code."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:upload'))
        self.assertEqual(response.status_code, 200)

    def test_new_note(self):
        """This should return a 200 status code and redirect to the dashboard and confirm the correct number of notes: 4"""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:upload'), {"title": "Note 7", "department": 1, "content": "Content 7"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.all().count(), 4)

    def test_unverified_user_note_client(self):
        """This should return a 406 status code as user is not in the department."""
        c = Client()
        c.login(username="user2", password="password2")
        response = c.post(reverse('notebook:upload'), {"title": "Note 5", "department": "1", "content": "Content 5"})
        self.assertEqual(response.status_code, 406)
    
    def test_invalid_new_note(self):
        """This should return a 406 status code due to invalid department."""
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
        """This should return a 302 status code and redirect to the note and confirm the correct number of notes: 3"""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        n = u.notes.all()[0]
        response = c.post(reverse('notebook:manage_note'), {"edit": n.id, "title": n.title, "department": n.department.id, "content": "Content 1 edited", "published": n.published})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notebook:note', args=[n.id]))
        self.assertEqual(Note.objects.all().count(), 3)
        self.assertEqual(u.notes.all()[0].content, 'Content 1 edited')

    def test_student_leader_edit_notes_of_other_user(self):
        """This should return a 302 status code as the student leader can edit notes of other users."""
        n = Note.objects.create(user=User.objects.get(username="user3"), title="Note 3", department=Department.objects.get(code='DEPMT1'), content="Content 3")
        self.assertEqual(Note.objects.all().count(), 4)
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:manage_note'), {"edit": n.id, "title": n.title, "department": n.department.id, "content": "Content 3 edited", "published": n.published})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('notebook:note', args=[n.id]))
        self.assertEqual(User.objects.get(username="user3").notes.all()[0].content, 'Content 3 edited')
    
    def test_invalid_edit_note(self):
        """This should return a 406 status code."""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        n = u.notes.all()[0]
        response = c.post(reverse('notebook:manage_note'), {"edit": n.id, "title": n.title, "department": 3, "content": "Content 1 edited", "published": n.published})
        self.assertEqual(response.status_code, 406)
        self.assertEqual(u.notes.all()[0].content, 'Content 1')
        
    def test_adding_file(self):
        """The file should be successfully added to the note with status code 200 and then replaced with the status code 200"""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        n = u.notes.all()[0]
        with open("notebook/test_files/test.txt", "rb") as fb:
            response = c.post(reverse('notebook:manage_note'), {
                            "edit": n.id, 
                            "title": n.title, 
                            "department": n.department.id, 
                            "content": n.content, 
                            "published": n.published, 
                            "file": fb
                            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(filecmp.cmp(u.notes.all()[0].file.path, "notebook/test_files/test.txt", shallow=True))
        with open("notebook/test_files/test1.txt", "rb") as fb:
            response = c.post(reverse('notebook:manage_note'), {
                            "edit": n.id, 
                            "title": n.title, 
                            "department": n.department.id, 
                            "content": n.content, 
                            "published": n.published, 
                            "file": fb
                            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(filecmp.cmp(u.notes.all()[0].file.path, "notebook/test_files/test1.txt", shallow=True))
    def test_clear_file(self):
        """The file should be successfully added and then removed from the note with status code 200"""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        n = u.notes.all()[0]
        with open("notebook/test_files/test.txt", "rb") as fb:
            response = c.post(reverse('notebook:manage_note'), {
                            "edit": n.id, 
                            "title": n.title, 
                            "department": n.department.id, 
                            "content": n.content, 
                            "published": n.published, 
                            "file": fb
                            })
            self.assertEqual(response.status_code, 302)
            self.assertTrue(bool(u.notes.all()[0].file))
        response = c.post(reverse('notebook:manage_note'), {
                        "edit": n.id, 
                        "title": n.title, 
                        "department": n.department.id, 
                        "content": n.content, 
                        "published": n.published, 
                        "file-clear": "on"
                        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(bool(u.notes.all()[0].file))
    
    def test_teams_member(self):
        """This should return status code 200 and correct number of teams"""
        c = Client()
        c.login(username="user2", password="password2")
        
        response = c.get(reverse('notebook:teams'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['teams'].count(),1)
        
        response = c.get(reverse('notebook:teams')+'?filter=all')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['teams'].count(),2)

    def test_valid_team_join(self):
        """This should return a 200 status code and user should be added to the waitlist"""
        #create user
        u4 = User.objects.create_user(username='user4', password='password4')
        u4.verified = True
        u4.position = 1
        u4.save()

        c = Client()
        c.login(username="user4", password="password4")
        d = Department.objects.get(code="DEPMT1")
        response = c.post(reverse('notebook:teams'),{
            "code":"DEPMT1",
            "action":"join"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(u4 in d.waitlist.all())
    
    def test_valid_team_leave(self):
        """This should return a 200 status code and user should be added to the waitlist"""
        c = Client()
        c.login(username="user1", password="password1")
        u = User.objects.get(username="user1")
        d = Department.objects.get(code="DEPMT1")
        response = c.post(reverse('notebook:teams'),{
            "code":"DEPMT1",
            "action":"leave"
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(u not in d.members.all())
        self.assertTrue(u not in d.leader.all())

    def test_team_users_list(self):
        """This should return 200 status code and 2 users in department 2"""
        c = Client()
        c.login(username='user1', password='password1')
        response = c.get(reverse('notebook:team',args=['DEPMT2']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['memberlist'].count(), 2)
    
    def test_team_waitlist(self):
        """This should return 200 status code with 1 user in waitlist"""
        c = Client()
        c.login(username='user1', password='password1')
        response = c.get(reverse('notebook:team', args=['DEPMT2'])+'?fetch=waitlist')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['memberlist'].count(), 1)
    
    def test_invalid_leader_add_user(self):
        """This should raise Permission Denied 403 as user1 is not leader of department 1"""
        c = Client()
        c.login(username='user1', password='password1')
        Department.objects.get(code='DEPMT1').waitlist.add(User.objects.get(username='user2'))
        response = c.post(reverse('notebook:team', args=['DEPMT1']),{
            'username':'user2',
            'action':'add'
        })
        self.assertEqual(response.status_code, 403)
    
    def test_valid_user_add_user(self):
        """This should return 302 status code and add user to members"""
        c = Client()
        c.login(username='user1', password='password1')
        u = User.objects.get(username='user3')
        d = Department.objects.get(code='DEPMT2')
        response = c.post(reverse('notebook:team',args=['DEPMT2']),{
            'username':'user3',
            'action':'add'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(u in d.members.all())

    def test_invalid_user_admin_access(self):
        """This should return a 403 status code."""
        c = Client()
        c.login(username="user2", password="password2")
        response1 = c.get(reverse('notebook:admin'))
        c.logout()
        c.login(username="user3", password="password3")
        response2 = c.get(reverse('notebook:admin'))
        self.assertEqual(response1.status_code, 403)
        self.assertEqual(response2.status_code, 403)
    
    def test_valid_user_admin_access(self):
        """This should return a 200 status code."""
        c = Client()
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:admin'))
        self.assertEqual(response.status_code, 200)

    def test_user_position_update(self):
        """This should return a 302 status code and update the user2's position to 2."""
        c = Client()
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:admin'), {"username": "user2", "action": "update", "position": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username="user2").position, 2)
    
    def test_invalid_user_position_update(self):
        """This should return a 403 status code as user is not student leader and thus should not have access to update user position."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:admin'), {"username": "user3", "action": "update", "position": 2})
        self.assertEqual(response.status_code, 403)

    def test_invalid_position_update(self):
        """This should return a 406 status code as the position is invalid."""
        c = Client()
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:admin'), {"username": "user2", "action": "update", "position": 4})
        self.assertEqual(response.status_code, 400)

    def test_invalid_position_update_of_student_leader(self):
        """This should return a 406 status code as the position of student leader cannot be changed."""
        c = Client()
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        u = User.objects.get(username="user2")
        u.position = 3
        u.save()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:admin'), {"username": "user2", "action": "update", "position": 2})
        self.assertEqual(response.status_code, 400)

    def test_login_required_for_account(self):
        """This should return a 302 status code and redirect to the login page."""
        c = Client()
        response = c.get(reverse('notebook:account'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"..{reverse('notebook:login')[0:-1]}?next={reverse('notebook:account')}")

    def test_accounts_page(self):
        """This should return a 200 status code."""
        c = Client()
        u = User.objects.get(username="user1")
        u.position = 3
        u.save()
        c.login(username="user1", password="password1")
        response = c.get(reverse('notebook:account'))
        self.assertEqual(response.status_code, 200)
        c.logout()
        c.login(username="user2", password="password2")
        response = c.get(reverse('notebook:account'))
        self.assertEqual(response.status_code, 200)
        c.logout()
        c.login(username="user3", password="password3")
        response = c.get(reverse('notebook:account'))
        self.assertEqual(response.status_code, 200)

    def test_successful_name_change(self):
        """This should return a 200 status code and the name should be changed."""
        c = Client()
        c.login(username="user1", password="password1")
        response = c.post(reverse('notebook:account'), {"first_name": "User", "last_name": "One"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.get(username="user1").first_name, "User")
        self.assertEqual(User.objects.get(username="user1").last_name, "One")

    def test_valid_image_upload(self):
        """This should return a 200 status code and the image should be uploaded."""
        c = Client()
        c.login(username="user1", password="password1")
        with open("notebook/test_files/test.png", "rb") as fb:
            response = c.post(reverse('notebook:image_upload'), {"image": fb})
        fb.close()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AttachedImages.objects.all().count(), 1)
        self.assertTrue(filecmp.cmp(AttachedImages.objects.all()[0].image.path, "notebook/test_files/test.png", shallow=True))

    def test_invalid_image_upload(self):
        """This should return a 406 status code."""
        c = Client()
        c.login(username="user1", password="password1")
        with open("notebook/test_files/test.txt", "rb") as fb:
            response = c.post(reverse('notebook:image_upload'), {"image": fb})
        fb.close()
        self.assertEqual(response.status_code, 406)
        self.assertEqual(AttachedImages.objects.all().count(), 0)
        

    def test_valid_delete_image(self):
        """This should return a 200 status code and the uploaded image should be deleted."""
        c = Client()
        c.login(username="user1", password="password1")
        with open("notebook/test_files/test.png", "rb") as fb:
            response = c.post(reverse('notebook:image_upload'), {"image": fb})
        fb.close()
        self.assertEqual(response.status_code, 200)
        id = AttachedImages.objects.all()[0].id
        response = c.delete(reverse('notebook:image_upload'), json.dumps({"id": str(id)}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AttachedImages.objects.all().count(), 0)

    def test_invalid_user_delete_image(self):
        """This should return a 403 status code as the user deleting the image is not the owner of the image"""
        c = Client()
        c.login(username="user2", password="password2")
        with open("notebook/test_files/test.png", "rb") as fb:
            response = c.post(reverse('notebook:image_upload'), {"image": fb})
        fb.close()
        self.assertEqual(response.status_code, 200)
        id = AttachedImages.objects.all()[0].id
        c.logout()
        c.login(username="user1", password="password1")
        response = c.delete(reverse('notebook:image_upload'), json.dumps({"id": str(id)}))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(AttachedImages.objects.all().count(), 1)

    def test_invalid_deletion_non_existent_image(self):
        """This should return a 406 status code as the image does not exist"""
        c = Client()
        c.login(username="user1", password="password1")
        self.assertEqual(AttachedImages.objects.all().count(), 0)
        response = c.delete(reverse('notebook:image_upload'), json.dumps({"id": str(uuid.uuid4())}))
        self.assertEqual(response.status_code, 406)


