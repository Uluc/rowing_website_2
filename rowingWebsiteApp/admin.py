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
    list_display = ['description', 'asociated_event', 'thumbnail']

    def thumbnail(self, obj):
        return format_html('<img src="{}" style="width: 130px; \
                           height: 100px"/>'.format(obj.image.url))

    thumbnail.short_description = 'thumbnail'

    list_per_page = 15



class RecruitmentAdmin(admin.ModelAdmin):
    pass

class SponsorAdmin(admin.ModelAdmin):
    pass

class BannerAdmin(admin.ModelAdmin):
    
    list_display = ['title','recruitment_display' , 'about_display', 'schedule_display', 'sponsor_display']

    def recruitment_display(self, obj):
        return format_html('<img src="{}" style="width: 130px; \
                           height: 100px"/>'.format(obj.recruitment_Banner.url))

    def about_display(self, obj):
        return format_html('<img src="{}" style="width: 130px; \
                           height: 100px"/>'.format(obj.about_Bannerimage.url))

    def schedule_display(self, obj):
        return format_html('<img src="{}" style="width: 130px; \
                           height: 100px"/>'.format(obj.schedule_Banner.url))     

    def sponsor_display(self, obj):
        return format_html('<img src="{}" style="width: 130px; \
                           height: 100px"/>'.format(obj.sponsor.url))

    recruitment_display.short_description = 'Recruitment Page Banner'
    about_display.short_description = 'About Page Banner'
    schedule_display.short_description = 'Schedule Page Banner'
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
