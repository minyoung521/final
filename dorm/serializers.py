from rest_framework import serializers
from .models import (
    Dorm, OutingApply, Notice, Post, Comment,
    UserProfile, Inquiry, InquiryAnswer, Like
)

class DormSerializer(serializers.ModelSerializer):
    user_id   = serializers.IntegerField(source='user.id', read_only=True)
    username  = serializers.CharField(source='user.username', read_only=True)
    content   = serializers.CharField(
                  required=False,
                  allow_blank=True,
                  allow_null=True
              )
    class Meta:
        model  = Dorm
        fields = [
            'id','user_id','username','name','student_number',
            'content','gender','building_name','r_number',
            'position','is_available'
        ]

class OutingApplySerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = OutingApply
        fields = [
            'id', 'name', 'student_number', 'out_date', 'applied_at',
            'status', 'status_display'
        ]
        read_only_fields = ['applied_at', 'status', 'status_display']

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id','title','content','date']

class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title','content']

class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    anon_author = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','author_id','anon_author','content','created_at']

    def get_anon_author(self, obj):
        return f"{obj.author.id%10000:04d}"

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostSerializer(serializers.ModelSerializer):
    author_id  = serializers.IntegerField(source='author.id', read_only=True)
    anon_author = serializers.SerializerMethodField()
    comments   = CommentSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked   = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id','author_id','anon_author','title','content',
            'image','created_at','updated_at','comments',
            'like_count','is_liked'
        ]

    def get_anon_author(self, obj):
        return f"{obj.author.id%10000:04d}"

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return obj.likes.filter(user=user).exists()

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    full_name = serializers.CharField(read_only=True)
    is_staff = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['user_id','username','email','full_name',
                  'department','reward_point','penalty_point',
                  'is_staff','is_superuser']

    def get_is_staff(self, obj): return obj.user.is_staff
    def get_is_superuser(self, obj): return obj.user.is_superuser

class InquirySerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Inquiry
        fields = ['id','user_id','username','title','content','created_at','answer']

    def get_answer(self, obj):
        try:
            return InquiryAnswerSerializer(obj.inquiryanswer).data
        except InquiryAnswer.DoesNotExist:
            return None

class InquiryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['title','content']

class InquiryAnswerSerializer(serializers.ModelSerializer):
    admin_id = serializers.IntegerField(source='admin.id', read_only=True)
    admin_username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = InquiryAnswer
        fields = ['id','admin_id','admin_username','answer','answered_at']

class InquiryAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryAnswer
        fields = ['answer']
