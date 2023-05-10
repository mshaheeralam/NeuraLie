from django.db import models

# Create your models here.
class Info(models.Model):
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female')
    ]
    name = models.CharField(max_length=50, primary_key=True)
    age = models.IntegerField(default=0, blank=True, null=True)
    time = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=4, choices=gender_choices)
    interviewer = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Questions(models.Model):
    name = models.ForeignKey(Info, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    is_truthful = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['name', 'question'], name='unique_question')
        ]

    def __str__(self):
        return f"{self.name} - {self.question}"
