from rest_framework import serializers

from comment.models import Comment
from user_info.serializers import UserDescSerializer


class CommentChildrenSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    user = UserDescSerializer(read_only=True)

    class Meta:
        model = Comment
        exclude = [
            'parent',
            'article'
        ]


class CommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    user = UserDescSerializer(read_only=True)

    # HyperlinkedRelatedField 用于对外键关系，而 HyperlinkedIdentityField 用于对当前模型自身。
    article = serializers.HyperlinkedRelatedField(view_name='article-detail', read_only=True)
    article_id = serializers.IntegerField(write_only=True, allow_null=False, required=True)

    # parent 为父评论，用了嵌套序列化器 CommentChildrenSerializer 。
    # 注意这个序列化器的 Meta 用 exclude 来定义不需要的字段。
    # 由于我们希望父评论只能在创建时被关联，后续不能更改（很合理），
    # 因此覆写 def update(...) ，使得在更新评论时忽略掉 parent_id 参数。
    parent = CommentChildrenSerializer(read_only=True)
    parent_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    def update(self, instance, validated_data):
        validated_data.pop('parent_id', None)
        return super().update(instance, validated_data)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'created': {'read_only': True}}