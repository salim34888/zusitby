from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path(
        'profile/',
        views.UserProfileView.as_view(),
        name='profile'
    ),
    path(
        'profile/edit/',
        views.UserProfileEditView.as_view(),
        name='edit_profile'
    ),
    path(
        'register/',
        views.StudentRegistrationView.as_view(),
        name='student_registration',
    ),
    path(
        'enroll-course/',
        views.StudentEnrollCourseView.as_view(),
        name='student_enroll_course'
    ),
    path(
        'courses/',
        views.StudentCourseListView.as_view(),
        name='student_course_list'
    ),
    path(
        'course/<pk>/',
        (views.StudentCourseView.as_view()), # cache_page(60 * 15)(views.StudentCourseView.as_view()),
        name='student_course_detail'
    ),
    path(
        'course/<pk>/<module_id>/',
        (views.StudentCourseDetailView.as_view()), #cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),
        name='student_course_detail_module'
    ),
    path(
        'course/<pk>/<module_id>/test/',
        (views.ModuleQuestionsView.as_view()), # cache_page(60 * 15)(views.ModuleQuestionsView.as_view()),
        name='module_questions'
    ),
    path(
        'course/<pk>/<module_id>/code_questions/',
        (views.CodeQuestionView.as_view()), # cache_page(60 * 15)(views.ModuleQuestionsView.as_view()),
        name='code_questions'
    ),
    path(
        'leaderboard/',
        (views.UserListView.as_view()), # cache_page(60 * 15)(views.ModuleQuestionsView.as_view()),
        name='leaderboard'
    ),
]