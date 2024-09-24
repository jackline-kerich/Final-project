from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone  # Import timezone

class HealthMetrics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weight = models.FloatField()
    systolic = models.IntegerField(default=120)
    diastolic = models.IntegerField(default=70)
    sleep_hours = models.FloatField()
    date = models.DateField(default=timezone.now)  # Set a default value here
    
class MindfulnessActivity(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class GuidedMeditation(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio = models.FileField(upload_to='guided_meditations/')

    def __str__(self):
        return self.title

class Soundscape(models.Model):
    title = models.CharField(max_length=200)
    audio = models.FileField(upload_to='soundscapes/')

    def __str__(self):
        return self.title

class MindfulMovement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='mindful_movements/')

    def __str__(self):
        return self.title

class GratitudeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Affirmation(models.Model):
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class MoodEntry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('stressed', 'Stressed'),
        ('tired', 'Tired'),
        ('anxious', 'Anxious'),
        ('content', 'Content'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mood = models.CharField(max_length=20, choices=MOOD_CHOICES)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.mood} on {self.date}"

class MindfulnessChallenge(models.Model):
    description = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.description

class CommunityPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

    def __str__(self):
        return self.user.username
    
class Post(models.Model):
    title = models.CharField(max_length=200)  # Make sure the 'title' field exists
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Ensure Post is defined
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10)  # e.g., 'like', 'love'

    class Meta:
        unique_together = ('post', 'user')

    
class EvidenceBasedInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('Pregnancy', 'Pregnancy'),
        ('Childbirth', 'Childbirth'),
        ('Postpartum', 'Postpartum Recovery'),
        ('Infant Care', 'Infant Care')
    ])
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

