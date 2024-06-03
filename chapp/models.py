from django.db import models
from django.contrib.auth.models import User

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True ,related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True , related_name='received_messages')
    content = models.TextField()
    date_of_message = models.DateTimeField(auto_now_add=True)
