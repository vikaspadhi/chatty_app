from django.db import models
from .managers import ThreadManager

# Create your models here.
class Thread(models.Model):
    THREAD_TYPE = (
        ('personal', 'Personal'),
        ('group', 'Group')
    )
    name = models.CharField(max_length=50, null=True, blank=True)
    thread_type = models.CharField(max_length=15, choices=THREAD_TYPE, default='group')
    users = models.ManyToManyField('account.User')

    objects = ThreadManager()

    def __str__(self) -> str:
        return f'{self.id}'

class Chat(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey('account.User', on_delete=models.CASCADE)
    text = models.TextField(blank=False, null=False)

    def __str__(self) -> str:
        return f'From <Thread - {self.thread}>'