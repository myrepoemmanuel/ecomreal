from webbrowser import get
from django import db
from django.test import TestCase
from django.contrib.auth import get_user_model

# Create your tests here.

class UserAccountTests(TestCase):
    def test_new_superuser(self):
        db = get_user_model()
        super_user = db.objects.create_superuser(
            'testuser@super.com', "user_name", 'full_name', 'password'
        )
        self.assertEqual(super_user.email, 'testuser@super.com')
        self.assertEqual(super_user.user_name, 'user_name')
        self.assertEqual(super_user.full_name, 'full_name')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertEqual(str(super_user), 'user_name')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='testuser@super.com', user_name='user_name1', full_name='fullnme', password='password', is_superuser=False)
        
        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='testuser@super.com', user_name='user_name1', full_name='fullnme', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='', user_name='user_name1', full_name='fullnme', password='password', is_superuser=True)

    def test_new_user(self):
        db = get_user_model()
        user = db.objects.create_user(
            'testuser@user.com', "user_name", 'full_name', 'password'
        )
        self.assertEqual(user.email, 'testuser@user.com')
        self.assertEqual(user.user_name, 'user_name')
        self.assertEqual(user.full_name, 'full_name')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(email='', user_name='user_n1', full_name='fullnme', password='password')


