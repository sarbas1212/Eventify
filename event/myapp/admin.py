from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import HeroBanner,Service,ServiceType,Booking

@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_editable = ('is_active',)
    list_filter = ('is_active',)


admin.site.register(Service)
admin.site.register(ServiceType)
admin.site.register(Booking)