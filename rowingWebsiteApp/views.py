from django.shortcuts import render
from django.http import HttpResponse
from .models import Race, Leadership, Event, Rower, Sponsor, Picture, Gallery, SponsorPage, HomePage, AboutPage, RecruitmentPage, PageBanners
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile
from django.db.models import F  
from django.core.mail import send_mail


emailAddress = 'reauxtigers@gmail.com'
# Create your views here.



class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)

def home(request):
    data = {
        'nbar' : 'home',
        'homeText' : HomePage.objects.all(),
        'banner' : PageBanners.objects.all()
    }

    if request.method == "POST":
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message = request.POST['message']

        send_mail(
            'Website Inquiry from ' + message_name,
            message + ' Related Email Address: ' + message_email,
            message_email,
            [emailAddress],
        )

        return render(request, 'rowingWebsiteApp/confirmationPage.html')
    else:
        return render(request, 'rowingWebsiteApp/homePage.html', data)

def aboutus(request):
    data={
        'nbar' : 'aboutus',
        'aboutText' : AboutPage.objects.all(),
        'banner' : PageBanners.objects.all()
    }
    
    return render(request, 'rowingWebsiteApp/aboutUsPage.html', data)

def confirmed(request):
    return render(request, 'rowingWebsiteApp/confirmationPage.html')

def photogallery(request):
    data = {
        'nbar' : 'photos',
        'gallery' : Gallery.objects.all()
    }
    return render(request, 'rowingWebsiteApp/photoGalleryPage.html', data )

def roster(request):
    data={
        'nbar' : 'roster' , 
        'rower' : Rower.objects.all()
    }
    return render(request, 'rowingWebsiteApp/rosterPage.html', data)

def schedule(request):
    data = {
        'nbar' : 'schedule',
        'races' : Race.objects.all().order_by(F('date').asc(nulls_last=True)),
        'banner' : PageBanners.objects.all()
    }
    return render(request, 'rowingWebsiteApp/schedulePage.html', data)
    
def sponsor(request):
    data = {
        'nbar' : 'sponsor',
        'sponsors' : Sponsor.objects.all(),
        'sponsorText' : SponsorPage.objects.all(),
        'banner' : PageBanners.objects.all()
    }
    return render(request, 'rowingWebsiteApp/sponsorPage.html', data)

def recruitment(request):
    data = {
        'nbar' : 'recruitment',
        'events' : Event.objects.all(),
        'recruitmentText' : RecruitmentPage.objects.all(),
        'banner' : PageBanners.objects.all()
        
    }
    return render(request, 'rowingWebsiteApp/recruitmentPage.html', data)

def leadership(request):
    data = {
        'nbar' : 'leadership',
        'leadership' : Leadership.objects.all()
    }
    return render(request, 'rowingWebsiteApp/leadershipPage.html', data )