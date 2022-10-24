from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from mainapp.models import News, Course, Lesson, CourseTeachers


admin.site.register(Course)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'deleted')
    list_filter = ('deleted', 'created_at')
    ordering = ('pk',)
    list_per_page = 5
    search_fields = ('title', 'preamble', 'body')
    actions = ('mark_as_delete',)

    def slug(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ', '-'),
            obj.title
        )

    slug.short_description = 'Слаг'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)

    mark_as_delete.short_description = 'Пометить удалённым'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_course_name', 'num', 'title', 'deleted']
    list_filter = ['course', 'created_at', 'deleted']
    ordering = ['-course__name', '-num']
    list_per_page = 5
    actions = ['mark_deleted']
    search_fields = ['title', 'description']

    def get_course_name(self, obj):
        return obj.course.name

    get_course_name.short_description = _('Course')

    def mark_deleted(self, request, queryset):
        queryset.update(deleted=True)

    mark_deleted.short_description = _('Mark deleted')


@admin.register(CourseTeachers)
class CourseTeachersAdmin(admin.ModelAdmin):
    list_display = ['id', '__str__', 'get_courses']
    list_select_related = True

    def get_courses(self, obj):
        return ", ".join((i.name for i in obj.courses.all()))

    get_courses.short_description = _('Courses')
