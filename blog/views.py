from rest_framework import filters
from rest_framework import viewsets

from blog.models import Article, Category, Tag, Avatar
from blog.permissions import IsAdminUserOrReadOnly
from blog.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer, AvatarSerializer


# from blog.serializers import ArticleListSerializers, ArticleShowSerializers


# Create your views here.


# class ArticleShow(APIView):
#     """提供了对文章详情的获取、修改、删除的 3 个方法，以及 1 个用于获取单个文章 model 的辅助方法。
#     和之前说的一样，DRF 类视图与传统 Django 的区别，.get() 、 .put() 就是多了一个将对象序列化（或反序列化）的步骤。
#     .delete() 方法因为不用返回实际数据，执行完删除动作就OK了。"""
#     """序列化器 serializer 不仅可以将数据进行序列化、反序列化，还包含数据验证、错误处理、数据库操作等能力。
#     序列化这个概念与具体语言无关。Python 或 JavaScript 对象转换为 Json 都称为序列化，反之为反序列化。
#     Json 是两种语言传输信息的桥梁，一但信息到达，对方都需要将其还原为自身的数据结构。"""
#     def get_object(self, pk):
#         """获取单个文章对象"""
#         # pk 即主键，默认状态下就是 id
#         try:
#             return Article.objects.get(pk=pk)
#         except:
#             return Http404
#
#     def get(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleShowSerializers(article)
#         # 返回 Json 数据
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         article = self.get_object(pk)
#         serializer = ArticleShowSerializers(article, data=request.data)
#         # 验证提交的数据是否合法
#         # 不合法则返回400
#         if serializer.is_valid():
#             # 序列化器将持有的数据反序列化后，
#             # 保存到数据库中
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         article = self.get_object(pk)
#         article.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class ArticleShow(mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   generics.GenericAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleShowSerializers
#     permission_classes = [IsAdminUserOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


# 更简单的做法：
# class ArticleShow(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleShowSerializers
#     permission_classes = [IsAdminUserOrReadOnly]
#
#
# class List(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     serializer_class = ArticleListSerializers
#     permission_classes = [IsAdminUserOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
# @api_view(['GET', 'POST'])
# def list(request):
#     if request.method == 'GET':
#         articles = Article.objects.all()
#         serializer = ArticleListSerializers(articles, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = ArticleListSerializers(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    # 完全匹配
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['user__username', 'title']
    # 模糊匹配
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'title']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(user__username=username)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    pagination_class = None
    # 多对多关系，DRF 默认你必须先得有这个外键对象，才能指定其关系。虽然也合情合理，
    # 但我们更希望在创建、更新文章时，程序会自动检查数据库里是否存在当前标签。
    # 如果存在则指向它，如果不存在则创建一个并指向它。


class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
