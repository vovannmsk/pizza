from django.contrib import admin

# Register your models here.
from .models import Pizza, TypeOfProduct, Buyers, Feedbacks


class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'ingredients', 'currentPrice', 'photo', 'is_ready', 'type_product')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'ingredients')
    list_editable = ('is_ready',)
    list_filter = ('is_ready', 'type_product')
    prepopulated_fields = {'slug': ('name',)}


class TypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'nameOfType')
    list_display_links = ('id', 'nameOfType')
    search_fields = ('nameOfType',)
    prepopulated_fields = {'slug': ('nameOfType',)}


class BuyersAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phoneNumber', 'address')
    list_display_links = ('id', 'name')


class FeedbacksAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'product', 'comment', 'user')
    list_display_links = ('id', 'buyer', 'product')
    ordering = ('-id',)


admin.site.register(Pizza, PizzaAdmin)
admin.site.register(TypeOfProduct, TypeAdmin)
admin.site.register(Buyers, BuyersAdmin)
admin.site.register(Feedbacks, FeedbacksAdmin)
