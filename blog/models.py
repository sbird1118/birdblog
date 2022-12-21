from django.contrib.auth.models import User
from django.db import models
from markdown import Markdown


# Create your models here.


class Category(models.Model):
    name = models.CharField("博客分类", max_length=100)
    index = models.IntegerField(default=999, verbose_name='分类排序')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name
        ordering = ['index']

    def __str__(self):
        return self.name


class Tag(models.Model):
    text = models.CharField("文章标签", max_length=100)

    class Meta:
        # verbose_text = '文章标签'
        # verbose_name_plural = '文章标签'
        ordering = ['-id']

    def __str__(self):
        return self.text


class Tui(models.Model):
    name = models.CharField('推荐位', max_length=100)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = '推荐位'

    def __str__(self):
        return self.name


class Avatar(models.Model):
    content = models.ImageField(upload_to='avatar/%Y%m%d')


class Article(models.Model):
    # 标题
    title = models.CharField('文章标题', max_length=100)
    # 摘要
    excerpt = models.CharField('摘要', max_length=100)
    # 分类
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 verbose_name='分类',
                                 related_name='articles',
                                 blank=True, null=True)
    # 标签
    tags = models.ManyToManyField(Tag, verbose_name='标签', related_name='articles', blank=True)
    # 图片
    # img = models.ImageField(upload_to='article_img/%Y/%m/%d', verbose_name='文章图片',
    #                         blank=True, null=True)
    # 标题图
    avatar = models.ForeignKey(
        Avatar,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='article'
    )
    # 正文
    body = models.TextField()
    # 作者
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE,
                             related_name='articles', verbose_name='作者')
    """
    文章作者，这里User是从django.contrib.auth.models导入的。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    """
    # 阅读量
    views = models.PositiveIntegerField('阅读量', default=0)
    # 推荐位
    # tui = models.ForeignKey(Tui, on_delete=models.DO_NOTHING, verbose_name='推荐位', blank=True, null=True)
    # 创建时间
    create_time = models.DateTimeField('发布时间', auto_now_add=True)
    # 更新时间
    modified_time = models.DateTimeField('修改时间', auto_now_add=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-create_time']

    def __str__(self):
        return self.title

    # 新增方法，将 body 转换为带 html 标签的正文
    # 方法返回了包含了两个元素的元组，分别为已渲染为 html 的正文和目录。
    def get_md(self):
        md = Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ]
        )
        md_body = md.convert(self.body)
        # toc 是渲染后的目录
        return md_body, md.toc


class Banner(models.Model):
    text_info = models.CharField('标题', max_length=50, default='')
    img = models.ImageField('轮播图', upload_to='banner/')
    link_url = models.URLField('图片链接', max_length=100)
    is_active = models.BooleanField('是否active', default=False)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'


class Link(models.Model):
    name = models.CharField('链接名称', max_length=20)
    link_url = models.URLField('网址', max_length=100)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'

    def __str__(self):
        return self.name
