from rest_framework import serializers
from .models import Grade, Subject, Chapter, Topic, Subtopic, Question

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    grade = serializers.CharField()

    class Meta:
        model = Subject
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        grade_name = ret.get('grade')
        if grade_name:
            try:
                ret['grade'] = Grade.objects.get(name=grade_name)
            except Grade.DoesNotExist:
                raise serializers.ValidationError({'grade': f'Grade "{grade_name}" does not exist.'})
        return ret

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['grade'] = instance.grade.name if instance.grade else None
        return rep

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
