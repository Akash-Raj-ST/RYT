from django.contrib import admin

from django.urls import reverse
from django.utils.safestring import mark_safe
# Register your models here.
from .models import Accounts, Places, Review, Place_map, Review_like, Review_pic, Review_tag
# Register your models here.
@admin.register(Accounts)
class AdminAccounts(admin.ModelAdmin):
    list_display = ("user_id","username","verified","dp")
    list_filter = ("verified",)
    list_editable = ("verified","dp")

@admin.register(Places)
class AdminPlaces(admin.ModelAdmin):
    list_display = ("p_id","place_name","subject","place_type","image","link")
    list_filter = ("place_type",)
    search_fields = ("place_name__startswith",)
    list_editable = ("place_type","image")

@admin.register(Place_map)
class AdminPlace_map(admin.ModelAdmin):
    list_display = ("pm_id","m1_name","s1_name")

    def m1_name(self,obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_places_change", args=(obj.pm_id.p_id,)),
            obj.pm_id.place_name
        ))
    
    def s1_name(self,obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:api_places_change", args=(obj.spm_id.p_id,)),
            obj.spm_id.place_name
        ))

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    list_display = ("r_id","place_name","user_id")

    def place_name(self,obj):
        return obj.p_id.place_name

    def user_id(self,obj):
        return obj.u_id.user_id

admin.site.register(Review_like)
admin.site.register(Review_pic)
admin.site.register(Review_tag)

