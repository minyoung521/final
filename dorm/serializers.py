from rest_framework import serializers
from django.contrib.auth.models import User
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
        fields = ['id','title','content','image','date']

class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title','content','image']

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
    author_id   = serializers.IntegerField(source='author.id', read_only=True)
    anon_author = serializers.SerializerMethodField()
    comments    = CommentSerializer(many=True, read_only=True)
    like_count  = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked    = serializers.SerializerMethodField()

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
    user_id      = serializers.IntegerField(source='user.id', read_only=True)
    username     = serializers.CharField(source='user.username', read_only=True)
    email        = serializers.CharField(source='user.email', read_only=True)
    full_name    = serializers.CharField(read_only=True)
    phone_number = serializers.CharField(read_only=True) 
    department   = serializers.CharField()
    reward_point = serializers.IntegerField()
    penalty_point= serializers.IntegerField()
    is_staff     = serializers.SerializerMethodField()
    is_superuser = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user_id','username','email','full_name','phone_number',
            'department','reward_point','penalty_point',
            'is_staff','is_superuser'
        ]

    def get_is_staff(self, obj): return obj.user.is_staff
    def get_is_superuser(self, obj): return obj.user.is_superuser

class InquiryAnswerSerializer(serializers.ModelSerializer):
    admin_id       = serializers.IntegerField(source='admin.id', read_only=True)
    admin_username = serializers.CharField(source='admin.username', read_only=True)

    class Meta:
        model = InquiryAnswer
        fields = ['id','admin_id','admin_username','answer','answered_at']

class InquirySerializer(serializers.ModelSerializer):
    user_id   = serializers.IntegerField(source='user.id', read_only=True)
    username  = serializers.CharField(source='user.username', read_only=True)
    answer    = serializers.SerializerMethodField()

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

class InquiryAnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InquiryAnswer
        fields = ['answer']

class UserAdminDetailSerializer(serializers.ModelSerializer):
    full_name    = serializers.CharField(source='userprofile.full_name', required=False, allow_blank=True)
    department   = serializers.CharField(source='userprofile.department', required=False, allow_blank=True)
    phone_number = serializers.CharField(source='userprofile.phone_number', required=False, allow_blank=True)
    student_number = serializers.CharField(source='username') 
    reward_point = serializers.IntegerField(source='userprofile.reward_point', required=False)
    penalty_point= serializers.IntegerField(source='userprofile.penalty_point', required=False)

    building_name  = serializers.SerializerMethodField()
    r_number       = serializers.SerializerMethodField()
    building_room  = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'full_name', 'student_number', 'department', 'phone_number',
            'reward_point', 'penalty_point', 'building_name', 'r_number', 'building_room'
        ]

    def get_building_name(self, obj):
        dorm = Dorm.objects.filter(user=obj).first()
        return dorm.building_name if dorm else ""

    def get_r_number(self, obj):
        dorm = Dorm.objects.filter(user=obj).first()
        return dorm.r_number if dorm else None

    def get_building_room(self, obj):
        dorm = Dorm.objects.filter(user=obj).first()
        if dorm and dorm.building_name:
            return f"{dorm.building_name} {dorm.r_number}호"
        return ""

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('userprofile', {})
        profile = getattr(instance, 'userprofile', None)
        if profile and profile_data:
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        dorm = Dorm.objects.filter(user=instance).first()
        dorm_updated = False
        request = self.context.get('request')
        if dorm and request and request.data:
            for field in ['building_name', 'r_number']:
                if field in request.data:
                    setattr(dorm, field, request.data[field])
                    dorm_updated = True
            if dorm_updated:
                dorm.save()

        return super().update(instance, validated_data)
