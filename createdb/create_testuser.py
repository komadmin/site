from django.contrib.auth.models import User

user = User.objects.create_user('testuser1', 'dprice80@gmail.com', 'password')
user.save()

user = User.objects.create_user('testuser2', 'dprice80@gmail.com', 'password')
user.save()
