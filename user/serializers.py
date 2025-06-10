from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreference
from questions.models import Grade, Subject, Chapter, Topic

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='user')
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        UserPreference.objects.create(user=user)
        return user

class UserPreferenceSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(required=False, allow_null=True, default="Grade 7")
    subjects = serializers.ListField(child=serializers.CharField(), required=False, default=["Maths"])
    chapters = serializers.ListField(child=serializers.CharField(), required=False, default=["Ch 1"])
    topics = serializers.ListField(child=serializers.CharField(), required=False, default=["Topic 1"])

    class Meta:
        model = UserPreference
        fields = ('grade', 'subjects', 'chapters', 'topics')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove all .choices assignments, keep as plain CharField/ListField
        # self.fields['grade'].choices = []
        # self.fields['subjects'].choices = []
        # self.fields['chapters'].choices = []
        # self.fields['topics'].choices = []

    def to_internal_value(self, data):
        # Convert names to objects
        ret = super().to_internal_value(data)
        # Grade
        grade_name = ret.get('grade')
        if grade_name:
            try:
                ret['grade'] = Grade.objects.get(name=grade_name)
            except Grade.DoesNotExist:
                raise serializers.ValidationError({'grade': f'Grade "{grade_name}" does not exist.'})
        # Subjects
        subject_names = ret.get('subjects', [])
        if subject_names:
            subjects = []
            for name in subject_names:
                try:
                    subjects.append(Subject.objects.get(name=name))
                except Subject.DoesNotExist:
                    raise serializers.ValidationError({'subjects': f'Subject "{name}" does not exist.'})
            ret['subjects'] = subjects
        # Chapters
        chapter_names = ret.get('chapters', [])
        if chapter_names:
            chapters = []
            for name in chapter_names:
                try:
                    chapters.append(Chapter.objects.get(name=name))
                except Chapter.DoesNotExist:
                    raise serializers.ValidationError({'chapters': f'Chapter "{name}" does not exist.'})
            ret['chapters'] = chapters
        # Topics
        topic_names = ret.get('topics', [])
        if topic_names:
            topics = []
            for name in topic_names:
                try:
                    topics.append(Topic.objects.get(name=name))
                except Topic.DoesNotExist:
                    raise serializers.ValidationError({'topics': f'Topic "{name}" does not exist.'})
            ret['topics'] = topics
        return ret

    def update(self, instance, validated_data):
        # Handle grade (FK)
        grade = validated_data.pop('grade', None)
        if grade is not None:
            instance.grade = grade
        # Handle subjects (M2M)
        subjects = validated_data.pop('subjects', None)
        if subjects is not None:
            if hasattr(subjects, 'all'):
                subjects = list(subjects.all())
            elif isinstance(subjects, (list, tuple, set)):
                subjects = list(subjects)
            else:
                subjects = list(subjects) if subjects else []
            instance.subjects.set(subjects)
        # Handle chapters (M2M)
        chapters = validated_data.pop('chapters', None)
        if chapters is not None:
            if hasattr(chapters, 'all'):
                chapters = list(chapters.all())
            elif isinstance(chapters, (list, tuple, set)):
                chapters = list(chapters)
            else:
                chapters = list(chapters) if chapters else []
            instance.chapters.set(chapters)
        # Handle topics (M2M)
        topics = validated_data.pop('topics', None)
        if topics is not None:
            if hasattr(topics, 'all'):
                topics = list(topics.all())
            elif isinstance(topics, (list, tuple, set)):
                topics = list(topics)
            else:
                topics = list(topics) if topics else []
            instance.topics.set(topics)
        instance.save()
        return instance

    def create(self, validated_data):
        # Handle grade (FK)
        grade = validated_data.pop('grade', None)
        # Handle M2M
        subjects = validated_data.pop('subjects', [])
        chapters = validated_data.pop('chapters', [])
        topics = validated_data.pop('topics', [])
        instance = UserPreference.objects.create(grade=grade, **validated_data)
        if isinstance(subjects, list):
            instance.subjects.set(subjects)
        elif subjects is not None:
            instance.subjects.set(list(subjects.all()))
        if isinstance(chapters, list):
            instance.chapters.set(chapters)
        elif chapters is not None:
            instance.chapters.set(list(chapters.all()))
        if isinstance(topics, list):
            instance.topics.set(topics)
        elif topics is not None:
            instance.topics.set(list(topics.all()))
        return instance

    def to_representation(self, instance):
        # Show names in output
        rep = {}
        rep['grade'] = instance.grade.name if instance.grade else None
        rep['subjects'] = [s.name for s in instance.subjects.all()]
        rep['chapters'] = [c.name for c in instance.chapters.all()]
        rep['topics'] = [t.name for t in instance.topics.all()]
        return rep

class UserSerializer(serializers.ModelSerializer):
    preference = UserPreferenceSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'preference')
