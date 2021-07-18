from django.db import models
import zipfile
from image_cropping.fields import ImageRatioField, ImageCropField
from django.conf import settings
from easy_thumbnails.fields import ThumbnailerImageField
from imagekit.models import ImageSpecField
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from zipfile import ZipFile
from sortedm2m.fields import SortedManyToManyField
from django.core.files.base import ContentFile
from django.utils.html import format_html
from django.utils.html import escape
from django.core.exceptions import ValidationError

class CustomManager(models.Manager):
    def delete(self):
        for obj in self.get_queryset():
            obj.delete()


class Rower(models.Model):

    ORIENTATION = (
        ('Starboard','Starboard'),
        ('Port', 'Port'),
        ('Bisweptual', 'Bisweptual'),
        ('Coxswain', 'Coxswain')
        )
    
    CREWS = (
        ('Mens', 'Mens'),
        ('Womens', 'Womens')
        )

    VARSITY = (
        ('Yes', 'Yes'),
        ('No', 'No')
        )
    
    YEAR = (
        ('Freshmen','FR'),
        ('Sophomore','SO'),
        ('Junior','JR'),
        ('Senior','SR')
    )

    

    first_name = models.CharField(max_length=64, blank=False)
    last_name = models.CharField(max_length=64)
    orientation = models.CharField(max_length=64, choices=ORIENTATION)
    hometown = models.CharField(max_length=64, help_text=("Example: Baton Rouge, LA"))
    major = models.CharField(max_length=64)
    picture = models.ImageField(upload_to = 'rowers')
    cropping = ImageRatioField('picture', '5x7')
    crew = models.CharField(max_length=64, choices=CREWS)
    varsity = models.CharField(max_length=64, choices=VARSITY)
    year = models.CharField(max_length=64, choices=YEAR)


    #displays the name
    def __str__(self):
        return self.first_name +" "+ self.last_name

    class Meta:
        ordering = ['last_name']

    objects = CustomManager() # just add this line of code inside of your model

    def delete(self, using=None, keep_parents=False):
        self.picture.storage.delete(self.picture.name)
        super().delete()

class Race(models.Model):

    SEMESTER = (
        ('Fall','Fall'),
        ('Spring','Spring'),
    )
    
    name = models.CharField(max_length=64)
    location= models.CharField(max_length=64, help_text=("Event address ex: 3355 Dalrymple Dr, Baton Rouge, LA 70802"))
    date = models.DateField(null=True, blank=True)
    semester = models.CharField(max_length=64, choices=SEMESTER)
    public = models.BooleanField(default = False, help_text=("When this is checked the race will be displayed on the website"))
    results = models.TextField(help_text=("List Event Results Here"),null=True, blank=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

class Event(models.Model):
    
    event = models.CharField(max_length=64)
    location= models.CharField(max_length=64, help_text=("Event address ex: 3355 Dalrymple Dr, Baton Rouge, LA 70802"))
    date = models.DateField(null=True, blank=True, help_text=("Select a date from the picker."))
    time= models.CharField(max_length=64, help_text=("Example: 3pm - 5pm"))
    public = models.BooleanField(default = False, help_text=("When this is checked the event will be displayed on the website"))

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.event

class Leadership(models.Model):
    
    STAFF = (
        ('Officer','Officer'),
        ('Coach', 'Coach'),
    )

    name = models.CharField(max_length=64)
    position = models.CharField(max_length=64)
    staff = models.CharField(max_length=64, choices=STAFF, default='Officer')
    picture = models.ImageField(upload_to = 'leadership');
    writeUp = models.TextField(help_text=("This will be the text that get displayed under the officer"))
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta(object):
        ordering = ['my_order']

    #displays the name
    def __str__(self):
        return self.name

class Sponsor(models.Model):
    
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    class Meta:
        ordering = ['last_name']

class Picture(models.Model):
    
    asociated_event = models.CharField(max_length=64, default='Picture', help_text=("Source of the event"))
    description = models.CharField(max_length=64, default='Picture', help_text=
    ("Describe your images so they can easily be identified to be added into appropriate gallery "))
    
    image = models.ImageField(upload_to='images')
    #image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFill(125, 125)], format='JPEG', options={'quality': 60})

    def __str__(self):
        return self.asociated_event + " - " + self.description

class Gallery(models.Model):
    title = models.CharField(max_length=64, help_text=("Name for the gallery"))
    date = models.DateField(help_text=("Date the event occured"))
    full_gallery_link = models.URLField(max_length=200, help_text="place google drive url here for the whole album", default='', blank= True)
    images = SortedManyToManyField(Picture)
    

    def __str__(self):
        return self.title

    class Meta: 
        verbose_name = "Gallery"
        verbose_name_plural = "Galleries"
        ordering = ['-date']

class HomePage(models.Model):
    
    title = models.CharField(max_length=32)
    text = models.TextField(help_text=("This will be the text that gets displayed"))
    image = models.ImageField(upload_to='template_photos')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)
    

    class Meta:
        ordering = ['my_order']
        verbose_name_plural = " Home Page Entries"
        
    def __str__(self):
        return self.title


class AboutPage(models.Model):
    
    title = models.CharField(max_length=32)
    text = models.TextField(help_text=("This will be the text that gets displayed"))
    image = models.ImageField(upload_to='template_photos')
    my_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['my_order']
        verbose_name_plural = " About Us Page Entries"

    def __str__(self):
        return self.title

class RecruitmentPage(models.Model):

    title = models.CharField(max_length=32)
    text = models.TextField(help_text=("This will be the text that gets displayed"))
    questionaire_link = models.CharField(max_length=128)
    image = models.ImageField(help_text=("This will be the image that gets displayed under the text"), upload_to='recruitmentPagePictures', default='none')

    class Meta:
        verbose_name_plural = " Recruitment Page Entries"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(RecruitmentPage, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class SponsorPage(models.Model):
    title = models.CharField(max_length=32)
    text = models.TextField(help_text=("This will be the text that gets displayed"))
    sponsorship_coordinator_name = models.CharField(max_length=64)
    sponsorship_coordinator_email = models.EmailField(max_length=254, help_text=("Refer to LSU email"))
    image = models.ImageField(upload_to='template_photos')

    class Meta:
        verbose_name_plural = " Sponsor Page Entries"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SponsorPage, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class PageBanners(models.Model):

    title = models.CharField(max_length=50, blank=True)

    home_page_title = models.CharField(max_length=50, default="Welcome To LSU Rowing")
    home_Banner = models.ImageField(upload_to='banners', default='')
    image_thumbnail_home = ImageSpecField(source='home_Banner', processors=[ResizeToFill(300, 200)], format='JPEG', options={'quality': 60})
    
    recruitment_page_title = models.CharField(max_length=50)
    recruitment_Banner = models.ImageField(upload_to='banners')
    image_thumbnail_recruitment = ImageSpecField(source='recruitment_Banner', processors=[ResizeToFill(300, 200)], format='JPEG', options={'quality': 60})
    
    about_page_title = models.CharField(max_length=50)
    about_Banner = models.ImageField(upload_to='banners')
    image_thumbnail_about = ImageSpecField(source='about_Banner', processors=[ResizeToFill(300, 200)], format='JPEG', options={'quality': 60})
    
    schedule_page_title = models.CharField(max_length=50)
    schedule_Banner = models.ImageField(upload_to='banners')
    image_thumbnail_schedule = ImageSpecField(source='schedule_Banner', processors=[ResizeToFill(300, 200)], format='JPEG', options={'quality': 60})
   
    sponsor_page_title = models.CharField(max_length=50)
    sponsor_Banner = models.ImageField(upload_to='banners')
    image_thumbnail_sponsor = ImageSpecField(source='sponsor_Banner', processors=[ResizeToFill(300, 200)], format='JPEG', options={'quality': 60})

    def __str__(self):
        return "Website Banners"
    
    class Meta:
        verbose_name_plural = "     Page Banners"