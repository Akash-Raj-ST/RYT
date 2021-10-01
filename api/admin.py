from django.contrib import admin

# Register your models here.
from .models import Accounts, Places, Review, Place_map, Review_like, Review_pic, Review_tag
# Register your models here.
admin.site.register(Accounts)
admin.site.register(Places)
admin.site.register(Place_map)

admin.site.register(Review)
admin.site.register(Review_like)
admin.site.register(Review_pic)
admin.site.register(Review_tag)

