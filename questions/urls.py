from rest_framework.routers import DefaultRouter
from .views import (
    GradeViewSet, SubjectViewSet, ChapterViewSet, TopicViewSet, SubtopicViewSet, QuestionViewSet
)

router = DefaultRouter()
router.register(r'grades', GradeViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'chapters', ChapterViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'subtopics', SubtopicViewSet)
router.register(r'questions', QuestionViewSet)

urlpatterns = router.urls
