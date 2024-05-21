from django.db import models
from django.contrib.auth.models import User
from Base.models import Profile
# Create your models here.
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
    reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")

    message = models.CharField(max_length=10000000000)

    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date']
        verbose_name_plural = "Message"

    def __str__(self):
        return f"{self.sender} - {self.reciever}"

    @property
    def sender_profile(self):
        sender_profile = Profile.objects.get(user=self.sender)
        return sender_profile
    @property
    def reciever_profile(self):
        reciever_profile = Profile.objects.get(user=self.reciever)
        return reciever_profile