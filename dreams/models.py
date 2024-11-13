from django.db import models
from my_account.models import CustomUser


class Dream(models.Model):
    title = models.CharField(max_length=255)
    short_descriptions = models.CharField(max_length=510, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.ManyToManyField(CustomUser, related_name="liked_dreams", blank=True)
    tags = models.ManyToManyField("Tag", related_name="tags", blank=True)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Цільова сума збору
    current_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Поточна сума збору
    status = models.CharField(max_length=20, choices=[('active', 'Активний'), ('completed', 'Завершено')],default='active')  # Статус збору
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    dream = models.ForeignKey(Dream, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

