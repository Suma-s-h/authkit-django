from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Profile


class RegistrationTests(TestCase):
    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_successful_registration_creates_user_and_profile(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane@example.com',
            'username': 'janedoe',
            'password1': 'TestPass#2024',
            'password2': 'TestPass#2024',
            'agree_terms': True,
        })
        self.assertRedirects(response, reverse('dashboard'))
        user = User.objects.get(username='janedoe')
        self.assertEqual(user.email, 'jane@example.com')
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_registration_logs_user_in(self):
        self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane2@example.com',
            'username': 'janedoe2',
            'password1': 'TestPass#2024',
            'password2': 'TestPass#2024',
            'agree_terms': True,
        })
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_duplicate_email_rejected(self):
        User.objects.create_user('existing', 'taken@example.com', 'Password#1')
        response = self.client.post(reverse('register'), {
            'first_name': 'New',
            'last_name': 'User',
            'email': 'taken@example.com',
            'username': 'newuser',
            'password1': 'TestPass#2024',
            'password2': 'TestPass#2024',
            'agree_terms': True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already exists')

    def test_short_username_rejected(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'A',
            'last_name': 'B',
            'email': 'ab@example.com',
            'username': 'ab',
            'password1': 'TestPass#2024',
            'password2': 'TestPass#2024',
            'agree_terms': True,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'at least 3')

    def test_mismatched_passwords_rejected(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'email': 'jane3@example.com',
            'username': 'janedoe3',
            'password1': 'TestPass#2024',
            'password2': 'DifferentPass#1',
            'agree_terms': True,
        })
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_redirected_from_register(self):
        User.objects.create_user('authuser', 'a@a.com', 'pass12345!')
        self.client.login(username='authuser', password='pass12345!')
        response = self.client.get(reverse('register'))
        self.assertRedirects(response, reverse('dashboard'))


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'TestPass#2024')

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_successful_login_redirects_to_dashboard(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'TestPass#2024',
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_wrong_password_rejected(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'WrongPassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_authenticated_user_redirected_from_login(self):
        self.client.login(username='testuser', password='TestPass#2024')
        response = self.client.get(reverse('login'))
        self.assertRedirects(response, reverse('dashboard'))

    def test_open_redirect_blocked(self):
        response = self.client.post(reverse('login') + '?next=https://evil.com', {
            'username': 'testuser',
            'password': 'TestPass#2024',
        })
        # Should redirect to dashboard, not the external URL
        self.assertRedirects(response, reverse('dashboard'))

    def test_safe_next_url_honoured(self):
        response = self.client.post(reverse('login') + '?next=/accounts/profile/', {
            'username': 'testuser',
            'password': 'TestPass#2024',
        })
        self.assertRedirects(response, '/accounts/profile/')


class LogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'TestPass#2024')
        self.client.login(username='testuser', password='TestPass#2024')

    def test_logout_confirm_page_loads(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_logout_via_post(self):
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        # Confirm session is cleared
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_logout_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('logout')}")


class DashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'TestPass#2024')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

    def test_dashboard_loads_for_authenticated_user(self):
        self.client.login(username='testuser', password='TestPass#2024')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/dashboard.html')


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'testuser', 'test@example.com', 'TestPass#2024',
            first_name='Test', last_name='User',
        )
        self.client.login(username='testuser', password='TestPass#2024')

    def test_profile_page_loads(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_saves_user_fields(self):
        response = self.client.post(reverse('profile'), {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Hello world',
            'location': 'London',
            'phone': '',
            'website': '',
            'gender': '',
            'avatar_color': '#ff0000',
        })
        self.assertRedirects(response, reverse('profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.location, 'London')
        self.assertEqual(self.user.profile.avatar_color, '#ff0000')

    def test_duplicate_email_on_profile_rejected(self):
        User.objects.create_user('other', 'other@example.com', 'pass12345!')
        response = self.client.post(reverse('profile'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'other@example.com',
            'bio': '',
            'location': '',
            'phone': '',
            'website': '',
            'gender': '',
            'avatar_color': '#4f46e5',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'already used by another account')

    def test_profile_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class PasswordChangeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'OldPass#2024')
        self.client.login(username='testuser', password='OldPass#2024')

    def test_password_change_page_loads(self):
        response = self.client.get(reverse('password_change'))
        self.assertEqual(response.status_code, 200)

    def test_successful_password_change(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'OldPass#2024',
            'new_password1': 'NewPass#2024',
            'new_password2': 'NewPass#2024',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPass#2024'))

    def test_wrong_old_password_rejected(self):
        response = self.client.post(reverse('password_change'), {
            'old_password': 'WrongOldPass',
            'new_password1': 'NewPass#2024',
            'new_password2': 'NewPass#2024',
        })
        self.assertEqual(response.status_code, 200)

    def test_session_preserved_after_password_change(self):
        self.client.post(reverse('password_change'), {
            'old_password': 'OldPass#2024',
            'new_password1': 'NewPass#2024',
            'new_password2': 'NewPass#2024',
        })
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)


class PasswordResetTests(TestCase):
    def test_password_reset_page_loads(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_password_reset_redirects_on_valid_email(self):
        User.objects.create_user('resetuser', 'reset@example.com', 'TestPass#2024')
        response = self.client.post(reverse('password_reset'), {'email': 'reset@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_redirects_on_unknown_email(self):
        # Should always redirect — never reveal if email exists
        response = self.client.post(reverse('password_reset'), {'email': 'nobody@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))

    def test_password_reset_done_page_loads(self):
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_page_loads(self):
        response = self.client.get(reverse('password_reset_complete'))
        self.assertEqual(response.status_code, 200)


class ProfileModelTests(TestCase):
    def test_profile_auto_created_on_user_creation(self):
        user = User.objects.create_user('modeluser', 'model@example.com', 'TestPass#2024')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)

    def test_get_initials_with_full_name(self):
        user = User.objects.create_user('inituser', '', 'pass12345!',
                                        first_name='Alice', last_name='Brown')
        self.assertEqual(user.profile.get_initials(), 'AB')

    def test_get_initials_fallback_to_username(self):
        user = User.objects.create_user('noname', '', 'pass12345!')
        self.assertEqual(user.profile.get_initials(), 'NO')

    def test_profile_str(self):
        user = User.objects.create_user('struser', '', 'pass12345!')
        self.assertEqual(str(user.profile), 'struser Profile')

    def test_profile_deleted_with_user(self):
        user = User.objects.create_user('deluser', '', 'pass12345!')
        profile_id = user.profile.pk
        user.delete()
        self.assertFalse(Profile.objects.filter(pk=profile_id).exists())
