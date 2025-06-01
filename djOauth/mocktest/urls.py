from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubjectViewSet, QuestionViewSet, OptionViewSet

router = DefaultRouter()
router.register(r'subjects', SubjectViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
