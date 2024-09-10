from django.contrib import admin
from .models import Question,Choice
from django.utils.html import format_html


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('hahah',            {'fields': ['YEAR_IN_SCHOOL_CHOICES']}),
        ('Date information', {'fields': ['pub_date'],'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date','YEAR_IN_SCHOOL_CHOICES', 'was_published_recently','operator')
    list_filter = ['pub_date']
    search_fields = ['question_text']


    #  添加action动作选项
    # actions = ["mark_immortal"]
    # def mark_immortal(self, request, queryset):
    #     queryset.update(is_immortal=True)

    # def buttons(self, obj):
    #     button_html = """<a class="update_book" href="#">编辑</a>"""
    #     return format_html(button_html)
    #
    # buttons.short_description = "操作"


    def operator(self,obj):
        return format_html(
            '<a href="update_data/">更新<a/>'
        )
        operator.short_description = '数据更新'


admin.site.register(Question, QuestionAdmin)