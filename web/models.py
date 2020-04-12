from django.db import models


class Update(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    body = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        ftime = self.created.strftime('%H:%M, %d %b %Y')
        return f'Update {ftime}'
