from django.contrib.auth.models import UserManager as BaseUserManager


class UserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )

        user.save(using=self._db)
        return user
