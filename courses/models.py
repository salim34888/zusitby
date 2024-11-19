from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .fields import OrderField
from django.template.loader import render_to_string

class Subject(models.Model): # Раздел
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    logo = models.FileField(upload_to='images', default='images/mylife.jpg')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model): # Курс
    owner = models.ForeignKey(
        User,
        related_name='courses_created',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        Subject,
        related_name='courses',
        on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        User,
        related_name='courses_joined',
        blank=True
    )

    diff = {
        'EASY': 'EASY',
        'MIDDLE': 'MIDDLE',
        'HARD': 'HARD',
        'INSANE': 'INSANE',
    }

    pc = { # tipo project or course
        'Course': 'Course',
        'Project': 'Project',
    }

    title = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=6, choices=diff, default='EASY')
    pc = models.CharField(max_length=7, choices=pc, default='Course')
    logo = models.FileField(upload_to='images')
    is_done = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class Module(models.Model): # Тема
    course = models.ForeignKey(
        Course, related_name='modules', on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name='contents',
        on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'model_in':('text', 'video', 'image', 'file', 'question', 'code', 'tasks')
        }
    )
    
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])


    class Meta:
        ordering = ['order']


class ItemBase(models.Model):
    owner = models.ForeignKey(User,
        related_name='%(class)s_related',
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=250, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updates = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self}
        )

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()


class Question(models.Model): # write owner column
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    correct_answer = models.CharField(max_length=255)
    expected_output = models.TextField(blank=True, null=True)
    coins = models.IntegerField(default=10)

    def render(self):
        return render_to_string(
            f'courses/content/question.html',
            {'item': self}
        )


class Code(ItemBase):
    code = models.TextField()

