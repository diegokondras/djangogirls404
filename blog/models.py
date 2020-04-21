from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Sum


class Post(models.Model): # Utilizando Herança com Python Post é um Model
    # Definindo a chave estrangeira 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()


    create_date = models.DateField(auto_now=True)

    #definindo data e hora e o campo pode ser nulo
    published_date = models.DateField(blank=True, null=True)
    views = models.BigIntegerField(default=0)
    

    def publish(self):
        #Pega a data e hora atual e altera a data de publicação para realizar o salvamento de dados no banco de dados
        self.published_date = timezone.now()
        self.save()

    def __str__(self): #Retorna a string do objeto em memória
        return '{} ({})'.format(self.title, self.author)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


    def likes_count(self):

        count = self.opinion.aggregate(Sum('like'))

        if count['like__sum'] == None :
            count['like__sum'] = 0
    
        return count['like__sum'] #retorna a quantidade de PostLike no Post, como sendo filtro a proprio objeto Post

    def deslikes_count(self):
        count = self.opinion.aggregate(Sum('deslike'))

        if count['deslike__sum'] == None :
            count['deslike__sum'] = 0

        return count['deslike__sum']

class Opinion(models.Model):
    like = models.IntegerField(default=0)
    deslike = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='opinion')
    create_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return "'{}' '{}' '{}' '{}'".format(self.post.title, self.user,self.like,self.deslike)

class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "'{}' - '{}'".format(self.post.title, self.user)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text