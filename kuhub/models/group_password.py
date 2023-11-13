from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class GroupPassword(models.Model):
    group_password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        #collect password as hashed password.
        hashed_password = make_password(raw_password)
        self.group_password = hashed_password
        self.save()

    def check_password(self, raw_password):
        #check if the password is right or not.
        return check_password(raw_password, self.group_password)