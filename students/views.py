from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from courses.models import Course, Question, Module
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .forms import AnswerForm
from .models import UserProfile, UserAnswer
from django.views.generic import View
from django.template.response import TemplateResponse
from django.contrib import messages


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(
            username=cd['username'], password=cd['password1']
        )
        login(self.request, user)
        return result


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'student_course_detail', args=[self.course.id]
        )


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])


class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            # get first module
            context['module'] = course.modules.all()[0]
        return context


class ModuleQuestionsView(LoginRequiredMixin, View):
    template_name = 'students/course/question.html'

    def get_user_profile(self, user):
        profile, created = UserProfile.objects.get_or_create(user=user)
        return profile

    def get(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(Module, id=module_id)

        questions = Question.objects.filter(module=module)

        forms = []
        for question in questions:
            user_answer = UserAnswer.objects.filter(user=request.user, question=question, is_correct=True).first()

            if user_answer:
                forms.append((question, None))
            else:
                forms.append((question, AnswerForm(question=question)))

        return TemplateResponse(request, self.template_name, {
            'module': module,
            'forms': forms
        })

    def post(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(Module, id=module_id)
        user_profile = self.get_user_profile(request.user)
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id, module=module)

        user_answer = UserAnswer.objects.filter(user=request.user, question=question, is_correct=True).first()

        if user_answer:
            messages.info(request, 'Вы уже ответили правильно на этот вопрос.')
            return self.get(request, module_id)

        form = AnswerForm(request.POST, question=question)

        if form.is_valid():
            user_answer = form.cleaned_data['answer']
            is_correct = user_answer.lower() == question.correct_answer.lower()
            UserAnswer.objects.create(
                user=request.user,
                question=question,
                answer=user_answer,
                is_correct=is_correct
            )

            if is_correct:
                user_profile.points += 1
                messages.success(request, 'Ne Sosal')
            else:
                messages.error(request, 'V Sosal')

            user_profile.save()

        questions = Question.objects.filter(module=module)

        forms = []
        for question in questions:
            user_answer = UserAnswer.objects.filter(user=request.user, question=question, is_correct=True).first()

            if user_answer:
                forms.append((question, None))
            else:
                forms.append((question, AnswerForm(question=question)))

        return TemplateResponse(request, self.template_name, {
            'module': module,
            'forms': forms
        })