from django.urls import path

from . import views

app_name = 'tests'

urlpatterns = [
    path('tests/', views.tests, name='tests'),
    path('<int:test_id>/', views.display_test, name='display_test'),
    path('<int:test_id>/questions/<int:question_id>', views.display_question, name='display_question'),
    path('<int:test_id>/questions/<int:question_id>/grade/', views.grade_question, name='grade_question'),
    path('results/<int:test_id>/', views.test_results, name='test_results'),
]