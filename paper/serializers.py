from rest_framework import serializers
from questions.models import Question

class PaperGenerateSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(choices=[('subject', 'Subject'), ('chapter', 'Chapter'), ('topic', 'Topic'), ('subtopic', 'Subtopic')])
    value = serializers.ListField(child=serializers.CharField(), help_text="Name(s) of subject/chapter/topic/subtopic")
    question_type = serializers.CharField(default='mixed', help_text="mcq, msq, short, long, mixed (case-insensitive)")
    difficulty = serializers.CharField(default='mixed', help_text="easy, medium, hard, mixed (case-insensitive)")
    num_questions = serializers.IntegerField(min_value=1, help_text="Number of questions to generate")

    def validate_question_type(self, value):
        valid_types = [c[0] for c in Question.QUESTION_TYPE_CHOICES] + ['mixed']
        value_lower = value.lower()
        if value_lower not in valid_types:
            raise serializers.ValidationError(f"Invalid question_type. Valid options: {valid_types}")
        return value_lower

    def validate_difficulty(self, value):
        valid_diffs = [c[0] for c in Question.DIFFICULTY_CHOICES] + ['mixed']
        value_lower = value.lower()
        if value_lower not in valid_diffs:
            raise serializers.ValidationError(f"Invalid difficulty. Valid options: {valid_diffs}")
        return value_lower
