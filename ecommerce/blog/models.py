from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

class BlogManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(BlogManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
    return '%s/%s'%(instance.id, filename)

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True, width_field='width_field', height_field='height_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now_add=False, auto_now=False)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    objects = BlogManager()


    def __unicode__(self):
        return self.title

    #def get_absolute_url(self): We will replace it using reverse method with minor change
    #    return "/blog/%s/"%(self.id)

    def get_absolute_url(self):
        #return reverse('detail', kwargs={"id": self.id})
        return reverse('blog:detail', kwargs={"id": self.id}) #referring to the name space assigned to master urls.py

    class Meta:
        ordering = ['-timestamp', '-updated']

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exsits=qs.exists()
    if exsits:
        new_slug = "%s-%s"%(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)