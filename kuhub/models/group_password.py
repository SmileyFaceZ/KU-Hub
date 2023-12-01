from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class GroupPassword(models.Model):
    """
        A class representing the password for a group in Group Hub.

        Attributes:
            group_password(str): Hashed password for the group.

            set_password(raw_password): Set the group password by hashing the raw password.
            check_password(raw_password): Check if the provided raw password matches the hashed group password.

    """
    group_password = models.CharField(max_length=128)

    def set_password(self, raw_password):
        """
        Set the group password by hashing the raw password.
        """

        # collect password as hashed password.
        hashed_password = make_password(raw_password)
        self.group_password = hashed_password
        self.save()

    def check_password(self, raw_password):
        """
        Check if the provided raw password matches the hashed group password.

        Returns:
            bool: True when the password is correct.
        """
        # check if the password is right or not.
        return check_password(raw_password, self.group_password)
