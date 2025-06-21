from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserPreference
from questions.models import Grade, Subject, Chapter, Topic

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, default='user')
    password = serializers.CharField(write_only=True)
    grade = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'role', 'grade')

    def create(self, validated_data):
        grade_name = validated_data.pop('grade', None)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data.get('role', 'user')
        )
        grade_obj = None
        if grade_name:
            # Try exact match first
            grade_obj = Grade.objects.filter(name=grade_name).first()
            # If not found and input is digit, try 'Grade X'
            if not grade_obj and str(grade_name).isdigit():
                grade_obj = Grade.objects.filter(name=f"Grade {grade_name}").first()
        UserPreference.objects.create(user=user, grade=grade_obj)
        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Add grade to the registration response if available
        if hasattr(instance, 'preference') and instance.preference.grade:
            rep['grade'] = instance.preference.grade.name
        else:
            rep['grade'] = None
        return rep

class UserPreferenceSerializer(serializers.ModelSerializer):
    subjects = serializers.ListField(child=serializers.CharField(), required=False, default=["Maths"])
    chapters = serializers.ListField(child=serializers.CharField(), required=False, default=["Ch 1"])
    topics = serializers.ListField(child=serializers.CharField(), required=False, default=["Topic 1"])
    subtopics = serializers.ListField(child=serializers.CharField(), required=False, default=["Subtopic 1"])

    class Meta:
        model = UserPreference
        fields = ('subjects', 'chapters', 'topics', 'subtopics')

    def to_internal_value(self, data):
        # Convert names to objects
        ret = super().to_internal_value(data)
        # Subjects
        subject_names = ret.get('subjects', [])
        if subject_names:
            subjects = []
            for name in subject_names:
                subject = Subject.objects.filter(name=name).first()
                if subject:
                    subjects.append(subject)
                else:
                    raise serializers.ValidationError({'subjects': f'Subject "{name}" does not exist.'})
            ret['subjects'] = subjects
        # Chapters
        chapter_names = ret.get('chapters', [])
        if chapter_names:
            chapters = []
            for name in chapter_names:
                chapter = Chapter.objects.filter(name=name).first()
                if chapter:
                    chapters.append(chapter)
                else:
                    raise serializers.ValidationError({'chapters': f'Chapter "{name}" does not exist.'})
            ret['chapters'] = chapters
        # Topics
        topic_names = ret.get('topics', [])
        if topic_names:
            topics = []
            for name in topic_names:
                topic = Topic.objects.filter(name=name).first()
                if topic:
                    topics.append(topic)
                else:
                    raise serializers.ValidationError({'topics': f'Topic "{name}" does not exist.'})
            ret['topics'] = topics
        # Subtopics
        subtopic_names = ret.get('subtopics', [])
        if subtopic_names:
            subtopics = []
            for name in subtopic_names:
                from questions.models import Subtopic
                subtopic = Subtopic.objects.filter(name=name).first()
                if subtopic:
                    subtopics.append(subtopic)
                else:
                    raise serializers.ValidationError({'subtopics': f'Subtopic "{name}" does not exist.'})
            ret['subtopics'] = subtopics
        return ret

    def update(self, instance, validated_data):
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
        # Handle subtopics (M2M)
        subtopics = validated_data.pop('subtopics', None)
        if subtopics is not None:
            if hasattr(subtopics, 'all'):
                subtopics = list(subtopics.all())
            elif isinstance(subtopics, (list, tuple, set)):
                subtopics = list(subtopics)
            else:
                subtopics = list(subtopics) if subtopics else []
            instance.subtopics.set(subtopics)
        instance.save()
        return instance

    def create(self, validated_data):
        # Handle M2M
        subjects = validated_data.pop('subjects', [])
        chapters = validated_data.pop('chapters', [])
        topics = validated_data.pop('topics', [])
        subtopics = validated_data.pop('subtopics', [])
        instance = UserPreference.objects.create(**validated_data)
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
        if isinstance(subtopics, list):
            instance.subtopics.set(subtopics)
        elif subtopics is not None:
            instance.subtopics.set(list(subtopics.all()))
        return instance

    def to_representation(self, instance):
        # Show names in output
        rep = {}
        rep['subjects'] = [s.name for s in instance.subjects.all()]
        rep['chapters'] = [c.name for c in instance.chapters.all()]
        rep['topics'] = [t.name for t in instance.topics.all()]
        rep['subtopics'] = [st.name for st in instance.subtopics.all()]
        return rep

class UserSerializer(serializers.ModelSerializer):
    preference = UserPreferenceSerializer()
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'preference')

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'max_sub_users', 'parent']
