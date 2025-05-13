from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import *
from .forms import ProfileForm
from django.db.models import Q
from .models import User, Message
from .models import SkillListing, Agreement
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import User, Review



@login_required
def leave_review(request):
    if request.method == 'POST':
        reviewee_id = request.POST.get('reviewee_id')
        exchange_id = request.POST.get('exchange_id')  # Get the exchange ID

        reviewee = get_object_or_404(User, id=reviewee_id)
        exchange = get_object_or_404(Exchange, id=exchange_id)  # Get the exchange

        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if Review.objects.filter(reviewer=request.user, reviewee=reviewee, exchange=exchange).exists():
            messages.error(request, "You’ve already reviewed this user for this exchange.")
            return redirect('dashboard')

        Review.objects.create(
            reviewer=request.user,
            reviewee=reviewee,
            exchange=exchange,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Your review has been submitted!")
        return redirect('dashboard')

    return render(request, 'core/review.html')



def welcome_view(request):
    return render(request, 'core/welcome.html')

def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    listings = SkillListing.objects.all()
    return render(request, 'core/home.html', {'listings': listings})

@login_required
def profile_view(request):
    return render(request, 'core/profile.html')

@login_required
def post_skill(request):
    if request.method == 'POST':
        skill_id = request.POST.get('skill')
        description = request.POST.get('description')
        is_offer = request.POST.get('is_offer') == 'on'
        is_need = request.POST.get('is_need') == 'on'

        if not (is_offer or is_need):
            return render(request, 'core/post_skill.html', {
                'skills': Skill.objects.all(),
                'error': 'Please select if you are offering or looking for the skill.'
            })

        if skill_id == 'other':
            other_skill_name = request.POST.get('other_skill')
            if not other_skill_name:
                return render(request, 'core/post_skill.html', {
                    'skills': Skill.objects.all(),
                    'error': 'Please enter the custom skill name.'
                })
            skill, _ = Skill.objects.get_or_create(name=other_skill_name.strip())
        else:
            skill = Skill.objects.get(id=skill_id)

        # ✅ Create separate listings for offer and need
        if is_offer:
            SkillListing.objects.create(user=request.user, skill=skill, description=description, is_offer=True)
        if is_need:
            SkillListing.objects.create(user=request.user, skill=skill, description=description, is_offer=False)

        return redirect('home')

    return render(request, 'core/post_skill.html', {'skills': Skill.objects.all()})

@login_required
def message_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    # Show messages between the current user and the selected user
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )
            return redirect('messages', user_id=other_user.id)

    return render(request, 'core/message.html', {
        'messages': messages,
        'other_user': other_user
    })



@login_required
def leave_review(request):
    if request.method == 'POST':
        reviewee_id = request.POST.get('reviewee_id')
        reviewee = get_object_or_404(User, id=reviewee_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if Review.objects.filter(reviewer=request.user, reviewee=reviewee).exists():
            messages.error(request, "You’ve already reviewed this user.")
            return redirect('dashboard')

        Review.objects.create(
            reviewer=request.user,
            reviewee=reviewee,
            rating=rating,
            comment=comment
        )
        messages.success(request, "Your review has been submitted!")
        return redirect('dashboard')

    return render(request, 'core/review.html')


@login_required
def match_list(request):
    user_needs = SkillListing.objects.filter(user=request.user, is_offer=False)
    user_offers = SkillListing.objects.filter(user=request.user, is_offer=True)

    matches = []

    # You are looking for X → find who offers X
    for need in user_needs:
        potential = SkillListing.objects.filter(skill=need.skill, is_offer=True).exclude(user=request.user)
        matches.extend(potential)

    # You are offering Y → find who needs Y
    for offer in user_offers:
        potential = SkillListing.objects.filter(skill=offer.skill, is_offer=False).exclude(user=request.user)
        matches.extend(potential)

    # Remove duplicates
    matches = list({m.id: m for m in matches}.values())

    return render(request, 'core/match_list.html', {'matches': matches})


@login_required
def dashboard_view(request):
    agreements = Exchange.objects.filter(
        requester=request.user
    ).order_by('-start_date')[:5]  # latest 5
    return render(request, 'core/dashboard.html', {
        'agreements': agreements
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # or wherever your profile page is
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'core/edit_profile.html', {'form': form})

from django.db.models import Q

@login_required
def inbox_view(request):
    user = request.user

    # Get all users you've exchanged messages with
    conversations = Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values('sender', 'receiver')

    # Extract unique user IDs you've chatted with
    user_ids = set()
    for conv in conversations:
        user_ids.add(conv['sender'])
        user_ids.add(conv['receiver'])
    user_ids.discard(user.id)  # Remove yourself from the list

    chat_users = User.objects.filter(id__in=user_ids)

    return render(request, 'core/inbox.html', {'chat_users': chat_users})

@login_required
def edit_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)

    if request.method == 'POST':
        new_content = request.POST.get('content')
        if new_content:
            msg.content = new_content
            msg.edited = True
            msg.save()
        return redirect('messages', user_id=msg.receiver.id if msg.receiver != request.user else msg.sender.id)

    return render(request, 'core/edit_message.html', {'message': msg})


@login_required
def delete_message(request, message_id):
    msg = get_object_or_404(Message, id=message_id, sender=request.user)
    user_id = msg.receiver.id if msg.receiver != request.user else msg.sender.id
    msg.delete()
    return redirect('messages', user_id=user_id)



class AgreementForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ['responder', 'requested_skill', 'start_date', 'description']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional message or expectations...'}),
        }

@login_required
def create_agreement(request):
    if request.method == 'POST':
        form = AgreementForm(request.POST)
        if form.is_valid():
            agreement = form.save(commit=False)
            agreement.requester = request.user
            agreement.save()
            return redirect('dashboard')
    else:
        form = AgreementForm()

    return render(request, 'core/create_agreement.html', {'form': form})
