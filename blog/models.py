from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.CharField ( max_length=800 )
    author = models.CharField(max_length=15)
    slug = models.CharField(max_length=150)
    datestamp = models.DateTimeField(default=now)

    def __str__( self ):
        return  self.title + ' - ' + self.author

# Reply and Comment Models
class replyComment(models.Model):
    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE,null=True)
    timeStamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:10]+'..... '    + '- by ' + self.user.username