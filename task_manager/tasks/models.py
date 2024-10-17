from django.db import models
from ..statuses.models import Status
from ..users.models import User
from ..labels.models import Label

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    description = models.TextField(
        blank=True, 
        verbose_name='Description'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='status',
        verbose_name='Status',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name='Author',
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='performer',
        verbose_name='Performer',
    )
    labels = models.ManyToManyField(
        Label,
        related_name='label',
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name