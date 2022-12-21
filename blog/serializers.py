from rest_framework import serializers

from blog.models import Article, Category, Tag, Avatar
from comment.serializers import CommentSerializer
from user_info.serializers import UserDescSerializer


# class ArticleListSerializers(serializers.ModelSerializer):
#     url = serializers.HyperlinkedIdentityField(view_name='blog:show')
#     user = UserDescSerializer(read_only=True)
#
#     class Meta:
#         model = Article
#         fields = [
#             # 'id',
#             'url',
#             'title',
#             'excerpt',
#             'user',
#             'create_time',
#         ]
#         # read_only_fields = ['user']
#
#
# class ArticleShowSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
class ArticleCategoryDetailSerializer(serializers.ModelSerializer):
    """给分类详情的嵌套序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='article-detail')

    class Meta:
        model = Article
        fields = [
            'url',
            'title',
        ]


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    url = serializers.HyperlinkedIdentityField(view_name='category-detail')

    # HyperlinkedIdentityField前面章节有讲过，作用是将路由间的表示转换为超链接。
    # view_name参数是路由名，你必须显示指定。
    # category - detail是自动注册路由时，Router默认帮你设置的详情页面的名称，类似的还有category - list
    # 等，更多规则参考文档。
    class Meta:
        model = Category
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    """分类详情"""
    articles = ArticleCategoryDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'index',
            'articles',
        ]


class TagSerializer(serializers.HyperlinkedModelSerializer):
    """标签序列化器"""

    def check_tag_obj_exists(self, validated_data):
        text = validated_data.get('text')
        if Tag.objects.filter(text=text).exists():
            raise serializers.ValidationError('Tag with text {} exists.'.format(text))

    def create(self, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.check_tag_obj_exists(validated_data)
        return super().update(instance, validated_data)

    class Meta:
        model = Tag
        fields = '__all__'


class AvatarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='avatar-detail')

    class Meta:
        model = Avatar
        fields = '__all__'


class ArticleBaseSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = UserDescSerializer(read_only=True)
    # category 的嵌套序列化字段
    category = CategorySerializer(read_only=True)
    # category 的 id 字段，用于创建/更新 category 外键
    category_id = serializers.IntegerField(write_only=True, allow_null=True, required=False)

    # tag 字段默认的嵌套序列化器只显示外链的 id，需要改得更友好一些。
    # 但似乎又没必要改为超链接或者字段嵌套，因为标签就 text 字段有用。
    # 因此就用 SlugRelatedField 直接显示其 text 字段的内容就足够了。
    tags = serializers.SlugRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=False,
        slug_field='text'
    )

    # 覆写方法，如果输入的标签不存在则创建它
    def to_internal_value(self, data):
        tags_data = data.get('tags')

        if isinstance(tags_data, list):
            for text in tags_data:
                if not Tag.objects.filter(text=text).exists():
                    Tag.objects.create(text=text)

        return super().to_internal_value(data)

        # 图片字段

    avatar = AvatarSerializer(read_only=True)
    avatar_id = serializers.IntegerField(
        write_only=True,
        allow_null=True,
        required=False
    )
    # 自定义错误信息
    default_error_messages = {
        'incorrect_avatar_id': 'Avatar with id {value} not exists.',
        'incorrect_category_id': 'Category with id {value} not exists.',
        'default': 'No more message here..'
    }

    def check_obj_exists_or_fail(self, model, value, message='default'):
        if not self.default_error_messages.get(message, None):
            message = 'default'

        if not model.objects.filter(id=value).exists() and value is not None:
            self.fail(message, value=value)

    # 验证图片 id 是否存在
    # 不存在则返回验证错误
    def validate_avatar_id(self, value):
        self.check_obj_exists_or_fail(
            model=Avatar,
            value=value,
            message='incorrect_avatar_id'
        )
        return value

    # category_id 字段的验证器
    def validate_category_id(self, value):
        self.check_obj_exists_or_fail(
            model=Category,
            value=value,
            message='incorrect_category_id'
        )

        return value


class ArticleSerializer(ArticleBaseSerializer):
    """文章序列化器"""

    class Meta:
        model = Article
        fields = '__all__'
        extra_kwargs = {'body': {'write_only': True}}


class ArticleDetailSerializer(ArticleBaseSerializer):
    # 渲染后的正文
    body_html = serializers.SerializerMethodField()
    # 渲染后的目录
    toc_html = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    def get_body_html(self, obj):
        return obj.get_md()[0]

    def get_toc_html(self, obj):
        return obj.get_md()[1]

    class Meta:
        model = Article
        fields = '__all__'
