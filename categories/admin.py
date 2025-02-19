from django.contrib import admin
from categories.models import (
    Category,
    CategoryImage
)


class CategoryImageInLine(admin.TabularInline):
    model = CategoryImage
    extra = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryImageInLine]



