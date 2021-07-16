from django.contrib import admin
from django.contrib.admin import sites
from .models import Rower, Race, Leadership, Event, Sponsor, Picture, Gallery, HomePage, SponsorPage, RecruitmentPage, AboutPage, PageBanners
from image_cropping.admin import ImageCroppingMixin
from adminsortable2.admin import SortableAdminMixin
from imagekit.admin import AdminThumbnail
from django.utils.html import format_html

admin.site.site_header="LSU Rowing Website Manager"

class NoDeleteAdminMixin:
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

class MyModelAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ['get_name','crew', 'orientation']

    def get_name(self, obj):
        if obj.first_name:
            return obj.first_name + " " + obj.last_name
        else:
            return 'Not Available'

    get_name.short_description = 'Rower'

class AdminGallery(ImageCroppingMixin, admin.ModelAdmin):
    pass

class HomePageAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

class AboutUsAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

class MyModelAdminSorting(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'position', 'staff']

class FancyAdmin(admin.ModelAdmin):
    list_display = ['description', 'asociated_event', 'image_display']
    image_display = AdminThumbnail(image_field='image_thumbnail')
    image_display.short_description = 'Image'

    # set this to also show the image in the change view
    readonly_fields = ['image_display']
    list_per_page = 15



class RecruitmentAdmin(admin.ModelAdmin):
    pass

class SponsorAdmin(admin.ModelAdmin):
    pass

class BannerAdmin(admin.ModelAdmin):
    
    list_display = ['title','recruitment_display' , 'about_display', 'schedule_display', 'sponsor_display']
    

    recruitment_display = AdminThumbnail(image_field='image_thumbnail_recruitment')
    recruitment_display.short_description = 'Recruitment Page Banner'
    
    about_display = AdminThumbnail(image_field='image_thumbnail_about')
    about_display.short_description = 'About Page Banner'
    
    schedule_display = AdminThumbnail(image_field='image_thumbnail_schedule')
    schedule_display.short_description = 'Schedule Page Banner'

    sponsor_display = AdminThumbnail(image_field='image_thumbnail_sponsor')
    sponsor_display.short_description = 'Sponsor Page Banner'

    # def has_delete_permission(self, request, obj=None):
    #     return False
    # def has_add_permission(self, request):
    #    return False
    
admin.site.register(HomePage, HomePageAdmin)
admin.site.register(SponsorPage, SponsorAdmin)
admin.site.register(RecruitmentPage, RecruitmentAdmin)
admin.site.register(PageBanners, BannerAdmin)
admin.site.register(AboutPage, AboutUsAdmin)
admin.site.register(Sponsor)
admin.site.register(Rower, MyModelAdmin)
admin.site.register(Race)
admin.site.register(Leadership, MyModelAdminSorting)
admin.site.register(Event)
admin.site.register(Picture, FancyAdmin)
admin.site.register(Gallery)
