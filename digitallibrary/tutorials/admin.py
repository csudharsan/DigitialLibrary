from django.contrib import admin
from .models import SoftwareTutorials,Book

# Register your models here.

class SoftwareTutorialsAdmin(admin.ModelAdmin):
    class Meta:
        model = SoftwareTutorials


admin.site.register(SoftwareTutorials, SoftwareTutorialsAdmin)
admin.site.register(Book)