from django.db import models

#VALUE - DISPLAY
NATIONALITY_CHOICES = (
  ('US', 'UNITED STATES'),
  ('BR', 'BRAZIL')
)

class Actor(models.Model):
  name = models.CharField(max_length=200)
  birthday = models.DateField(null=True, blank=True)
  nationality = models.CharField(max_length=100, choices=NATIONALITY_CHOICES,
                                 blank=True, null=True)

  def __str__(self):
    return self.name
