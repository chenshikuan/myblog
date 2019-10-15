from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
# from ckeditor.fields import RichTextField #不能上传图片
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNum, ReadNumExpandMethod, ReadDetail
# Create your models here.

class BlogType(models.Model):
    type_name = models.CharField(max_length=10)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=100)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    # context = RichTextField(null=True)
    read_details = GenericRelation(ReadDetail) #让两个类产生关系
    context = RichTextUploadingField(null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)


    '''
        def get_read_num(self):
        try:
            return self.readnumber.read_num
        except exceptions.ObjectDoesNotExist:
            return '0'
    '''


    def __str__(self):
        return self.title

    class Meta:
        """
        function:order
        """
        ordering = ['-create_time']  # in reverse chronological order


"""
class ReadNumber(models.Model):
    read_num = models.IntegerField(default=0)
    blog = models.OneToOneField(Blog,on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.read_num)
"""