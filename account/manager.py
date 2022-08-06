from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,mobile,password=None,**extra_fileds):

        if not mobile:
            raise ValueError('Mobile number is required')
        
        user = self.model(mobile=mobile,**extra_fileds)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,mobile,password,**extra_fileds):
        extra_fileds.setdefault('is_staff',True)
        extra_fileds.setdefault('is_superuser',True)
        extra_fileds.setdefault('is_active',True)

        if extra_fileds.get('is_staff') is not True:
            raise ValueError('Super user must have is_staff true')

        return self.create_user(mobile,password,**extra_fileds)
