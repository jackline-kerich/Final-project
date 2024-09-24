from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import HealthMetrics, MindfulnessActivity, CommunityPost, EvidenceBasedInfo
from .forms import RegistrationForm, LoginForm  # Import both forms
from django.http import JsonResponse
from .models import HealthMetrics
from .forms import HealthMetricsForm
import json
from django.db.models import Count
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.utils import timezone
from datetime import timedelta
from .models import (
    MindfulnessActivity, GuidedMeditation, Soundscape, MindfulMovement,
    GratitudeEntry, Affirmation, MoodEntry, MindfulnessChallenge
)
from django.shortcuts import render, get_object_or_404,redirect
from .models import UserProfile
from .models import Post, Comment
from .forms import CommentForm

# Home view
def home_view(request):
    return render(request, 'nurturewell/home.html')

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(username=username, email=email, password=password)
            auth_login(request, user)  # Log the user in after registration
            return redirect('dashboard')  # Redirect to dashboard after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'nurturewell/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Log the user in
            return redirect('dashboard')  # Redirect to dashboard after login
    else:
        form = LoginForm()
    return render(request, 'nurturewell/login.html', {'form': form})

# Dashboard view
@login_required
def dashboard_view(request):
    health_metrics = HealthMetrics.objects.filter(user=request.user)
    context = {'health_metrics': health_metrics}
    return render(request, 'nurturewell/dashboard.html', context)

# Logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

# Health metrics view
@login_required
def health_metrics_view(request):
    if request.method == 'POST':
        form = HealthMetricsForm(request.POST)
        if form.is_valid():
            # Save data to the database for the logged-in user
            HealthMetrics.objects.create(
                weight=form.cleaned_data['weight'],
                systolic=form.cleaned_data['systolic'],
                diastolic=form.cleaned_data['diastolic'],
                sleep_hours=form.cleaned_data['sleep_hours'],
                user=request.user
            )
            return JsonResponse({'status': 'success'})
    
    # If it's a GET request or the form is invalid, render the HTML template for health metrics
    else:
        form = HealthMetricsForm()  # Create a new instance of the form for the GET request

    return render(request, 'nurturewell/health_metrics.html', {'form': form})

# View to fetch updated health data for Chart.js
@login_required
def get_health_metrics(request):
    metrics = HealthMetrics.objects.filter(user=request.user).order_by('date')  # Retrieve user-specific data

    # Extract data for the chart
    dates = [metric.date.strftime('%Y-%m-%d') for metric in metrics]  # Format dates
    weight_data = [metric.weight for metric in metrics]
    sleep_data = [metric.sleep_hours for metric in metrics]

    # Return data as JSON to be consumed by Chart.js
    return JsonResponse({
        'dates': dates,
        'weight': weight_data,
        'sleep': sleep_data
    })
# Mindfulness activities view
@login_required
def mindfulness_view(request):
    # Original mindfulness activities
    activities = MindfulnessActivity.objects.all()

    # New guided meditations, soundscapes, and mindful movements
    guided_meditations = GuidedMeditation.objects.all()
    soundscapes = Soundscape.objects.all()
    mindful_movements = MindfulMovement.objects.all()

    # Latest 5 gratitude entries by user
    gratitude_entries = GratitudeEntry.objects.filter(user=request.user).order_by('-date')[:5]

    # Random affirmation
    current_affirmation = Affirmation.objects.order_by('?').first().text if Affirmation.objects.exists() else 'Stay positive!'

    # Latest 5 mindfulness challenges
    mindfulness_challenges = MindfulnessChallenge.objects.order_by('-date')[:5]

    # Prepare mood data for the past 7 days
    today = timezone.now().date()
    dates = [today - timedelta(days=i) for i in range(6, -1, -1)]  # Past 7 days
    mood_data = []
    
    for date in dates:
        mood_counts = MoodEntry.objects.filter(user=request.user, date=date).values('mood').annotate(count=Count('mood'))
        mood_dict = {entry['mood']: entry['count'] for entry in mood_counts}
        mood_data.append({
            'date': DateFormat(date).format('M d'),
            'happy': mood_dict.get('happy', 0),
            'stressed': mood_dict.get('stressed', 0),
            'tired': mood_dict.get('tired', 0),
            'anxious': mood_dict.get('anxious', 0),
            'content': mood_dict.get('content', 0),
        })

    # Combine context
    context = {
        'activities': activities,  # Original activities
        'guided_meditations': guided_meditations,
        'soundscapes': soundscapes,
        'mindful_movements': mindful_movements,
        'gratitude_entries': gratitude_entries,
        'current_affirmation': current_affirmation,
        'mindfulness_challenges': mindfulness_challenges,
        'mood_data': json.dumps(mood_data)  # JSON data for mood visualization
    }

    return render(request, 'nurturewell/mindfulness.html', context)

# Save gratitude entry
@login_required
def save_gratitude(request):
    if request.method == 'POST':
        text = request.POST.get('gratitude_entry')
        if text:
            GratitudeEntry.objects.create(user=request.user, text=text)
    return redirect('mindfulness')

# Get random affirmation (AJAX)
@login_required
def get_affirmation(request):
    affirmation = Affirmation.objects.order_by('?').first()
    return JsonResponse({'affirmation': affirmation.text if affirmation else 'Stay positive!'})

# Save mood entry
@login_required
def save_mood(request):
    if request.method == 'POST':
        mood = request.POST.get('mood')
        if mood:
            MoodEntry.objects.create(user=request.user, mood=mood)
    return redirect('mindfulness')
# Community posts view
def community_view(request):
    posts = CommunityPost.objects.all()
    context = {'posts': posts}
    return render(request, 'nurturewell/community.html', context)

# Evidence-based information view
def evidence_info_view(request, category=None):
    if category:
        info_list = EvidenceBasedInfo.objects.filter(category=category)
    else:
        info_list = EvidenceBasedInfo.objects.all()
    context = {'info_list': info_list}
    return render(request, 'nurturewell/evidence_info.html', context)

def profile_view(request, username):
    user_profile = get_object_or_404(UserProfile, user__username=username)
    return render(request, 'nurturewell/profile.html', {'profile': user_profile})

@login_required  # To ensure only logged-in users can post comments
def post_detail_view(request, post_id):
    # Get the post by ID
    post = get_object_or_404(Post, id=post_id)
    
    # Get all related comments for the post
    comments = post.comments.all()

    # If the request is a POST method, process the comment form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a new comment without saving to the database yet
            comment = form.save(commit=False)
            comment.post = post  # Associate the comment with the post
            comment.user = request.user  # Associate the comment with the logged-in user
            comment.save()  # Save the comment to the database
            return redirect('post_detail', post_id=post.id)  # Redirect to the same post detail page after saving
    else:
        # If GET request, just show an empty form
        form = CommentForm()

    # Render the post detail template with post, comments, and form
    return render(request, 'nurturewell/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })
def react_to_post(request, post_id):
    # Get the post by ID
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        # Process the reaction, e.g., like or dislike
        reaction_type = request.POST.get('reaction')  # Assuming 'reaction' is passed in the form data

        # Here, you can implement your logic for handling reactions
        # For example, increasing like count, etc.
        if reaction_type == 'like':
            post.likes += 1
        elif reaction_type == 'dislike':
            post.dislikes += 1
        
        # Save the post after reaction
        post.save()

        # Redirect back to the post detail page
        return redirect('post_detail', post_id=post.id)

    # If not a POST request, redirect to post detail (or handle as needed)
    return redirect('post_detail', post_id=post.id)
def profile(request):
    return render(request, 'nurturewell/profile.html', {'profile': profile})

    