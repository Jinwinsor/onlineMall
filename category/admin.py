from django.contrib import admin
from .models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    # It will display slug after category name automatically
    list_display = ('category_name', 'slug')


admin.site.register(Category, CategoryAdmin)
