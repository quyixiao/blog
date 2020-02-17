from django.db import models

# Create your models here.
from user.models import User


class Post(models.Model):
    class Meta:
        db_table = 'bl_post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, null=False)
    pubdate = models.DateTimeField(null=False)
    # 作者
    # author_id = models.IntegerField(null=False)
    author = models.ForeignKey(User)

    # 内容

    def __repr__(self):
        return "<Post {} {} {} {} [{}] >".format(self.id, self.title,self.author,self.content,self.author.id)

    __str__ = __repr__


class Content(models.Model):
    class Meta:
        db_table = 'bl_content'

    # id 可以不写，主键django帮你创建一个pk
    post = models.OneToOneField(Post, to_field='id')  # post_id
    content = models.TextField(null=False)

    def __repr__(self):
        return "<Content {} {} {} >".format(self.id,self.post.id, self.content[:40])

    __str__ = __repr__
