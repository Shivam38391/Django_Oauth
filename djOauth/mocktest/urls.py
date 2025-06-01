from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MainCategoryViewSet, 
    SubjectViewSet, 
    QuestionViewSet, 
    OptionViewSet,
    TestResultViewSet
)

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'options', OptionViewSet)
router.register(r'results', TestResultViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
