from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from lms.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создаёт группу модераторов с нужными правами'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модераторы')

        course_ct = ContentType.objects.get_for_model(Course)
        lesson_ct = ContentType.objects.get_for_model(Lesson)

        permissions = Permission.objects.filter(
            content_type__in=[course_ct, lesson_ct],
            codename__in=['view_course', 'change_course', 'view_lesson', 'change_lesson']
        )

        group.permissions.set(permissions)

        self.stdout.write(self.style.SUCCESS(
            f"Группа 'Модераторы' {'создана' if created else 'обновлена'} с нужными правами."
        ))
