from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main = None
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                if main is not None:
                    raise ValidationError('Основной раздел должен быть один')
                main = form.cleaned_data['is_main']
        if main is None:
            raise ValidationError('Нет основного раздела')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    admin_list = ['id', 'name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    admin_list = ['id', 'title', 'published_at']
    filter_list = ['published_at']
    inlines = [ScopeInline]
