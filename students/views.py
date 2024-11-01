from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from courses.models import Course, Question, Module
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .forms import AnswerForm, UserProfileForm, UserForm, CodeForm
from .models import UserProfile, UserAnswer
from django.views.generic import View
from django.template.response import TemplateResponse
from django.contrib import messages
import sys
from io import StringIO
import re


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


class CodeQuestionView(LoginRequiredMixin, View):
    template_name = 'students/course/taks.html'

    def get(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(Module, id=module_id)
        questions = Question.objects.filter(module=module)

        forms = []
        for question in questions:
            user_answer = UserAnswer.objects.filter(user=request.user, question=question, is_correct=True).first()

            if user_answer:
                forms.append((question, None))
            else:
                forms.append((question, CodeForm()))

        return TemplateResponse(request, self.template_name, {
            'module': module,
            'forms': forms,
            'result': None,
        })

    def post(self, request, module_id, *args, **kwargs):
        module = get_object_or_404(Module, id=module_id)
        question_id = request.POST.get('question_id')
        question = get_object_or_404(Question, id=question_id, module=module)

        form = CodeForm(request.POST)

        execution_result = None

        if form.is_valid():
            user_code = form.cleaned_data['code']

            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()

            try:
                exec(user_code)
                execution_result = redirected_output.getvalue()
            except Exception as e:
                execution_result = f'Ошибка: {str(e)}'
            finally:
                sys.stdout = old_stdout

            if re.sub('\s+', '', execution_result) == re.sub('\s+', '', question.expected_output):
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    answer=user_code,
                    is_correct=True
                )

                user_profile, created = UserProfile.objects.get_or_create(user=request.user)
                user_profile.points += question.coins
                user_profile.save()

        forms = []
        questions = Question.objects.filter(module=module)
        for question in questions:
            user_answer = UserAnswer.objects.filter(user=request.user, question=question, is_correct=True).first()
            if user_answer:
                forms.append((question, None))
            else:
                forms.append((question, CodeForm()))

        return TemplateResponse(request, self.template_name, {
            'module': module,
            'forms': forms,
            'result': execution_result
        })


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
                user_profile.points += question.coins

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


class StudentCourseDetailView(CodeQuestionView, LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            context['module'] = course.modules.all()[0]
        return context


class StudentCourseView(LoginRequiredMixin, DetailView): # in future optimize this fucking code...
    model = Course
    template_name = 'students/course/module_view.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_object()
        if 'module_id' in self.kwargs:
            context['module'] = course.modules.get(
                id=self.kwargs['module_id']
            )
        else:
            context['module'] = course.modules.all()[0]
        return context


class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'students/student/account.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.userprofile


class UserProfileEditView(LoginRequiredMixin, View):
    template_name = 'students/student/account_edit.html'
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        return TemplateResponse(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return TemplateResponse(request, self.template_name, {
                'user_form': user_form,
                'profile_form': profile_form,
                'success_url': self.success_url  # Используем reverse_lazy для успешного URL
            })

        return TemplateResponse(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form
        })
