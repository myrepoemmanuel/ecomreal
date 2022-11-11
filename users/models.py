from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

User = settings.AUTH_USER_MODEL
    
# Create your models here.


class UserManager(BaseUserManager):
    def create_superuser(self, email, user_name, full_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        
        if other_fields.get('is_staff') is not True:
            raise ValueError("superuser must be assigned to is_staff=True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("superuser must be assigned to is_superuser=True")

        return self.create_user(email,user_name, full_name, password, **other_fields)



    def create_user(self, email, user_name, full_name, password, **other_fields):
        if not email:
            raise ValueError("User must have an email address")
        # if not password:
        #     raise ValueError("Users must have a password")
        
        email = self.normalize_email(email)
        user_obj = self.model(email=email, user_name=user_name, full_name=full_name, **other_fields)
            
        user_obj.set_password(password) #change password

        # user_obj.staff = is_staff
        # user_obj.admin = is_admin
        # user_obj.active = is_active
        user_obj.save()
        return user_obj


    # def create_staffuser(self, email, password=None):
    #     User = self.create_user(
    #         email,
    #         password=password,
    #         is_staff=True
    #         )
    #     return User

    # def create_superuser(self, email, password=None):
    #     User = self.create_user(
    #         email,
    #         password=password,
    #         is_staff=True,
    #         is_admin=True
    #         )
    #     return User



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    user_name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    about = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False) #can login
    is_staff = models.BooleanField(default=False) # regular staff user
    date_join = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #username

    #email and password are required by default
    REQUIRED_FIELDS = ['user_name', 'full_name']

    objects = UserManager()


    def __str__(self):
        return self.user_name

    # def get_full_name(self):
    #     return self.email

    # def get_short_name(self):
    #     return self.email

    # def has_perm(self, perm, obj=None):
    #     return True

    # def has_module_perms(self, app_label):
    #     return True

    # @property
    # def is_staff(self):
    #     return self.staff

    # @property
    # def is_admin(self):
    #     return self.admin

    # @property
    # def is_active(self):
    #     return self.active


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    address_one = models.CharField(max_length=200, null=True, blank=True)
    address_two = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    region = models.CharField(max_length=200, null=True, blank=True)
    
    
    
    def __str__(self):
        return f'{self.user.user_name} Profile'
#    
#    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, *args, **kwargs):
   if created:
       Profile.objects.create(user=instance, first_name=str(instance.full_name).split(" ")[0], last_name=str(instance.full_name).split(" ")[1])
       print(instance.user_name, 'Profile created')


@receiver(post_save, sender=User)
def save_profile(sender, instance, *args, **kwargs):
    instance.profile.save()






