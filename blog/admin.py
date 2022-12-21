from django.contrib import admin


# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'title', 'tui', 'user', 'views', 'create_time')
    list_per_page = 50
    ordering = ('-create_time',)
    list_display_links = ('id', 'title')


class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'text_info', 'img', 'link_url', 'is_active')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'index')


class TuiAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'link_url')
