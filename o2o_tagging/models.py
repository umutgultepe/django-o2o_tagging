from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from model_utils.managers import PassThroughManager

from .managers import O2OTagQuerySet


class O2OTag(models.Model):
    # The object that is tagging
    tagger_content_type = models.ForeignKey(ContentType,
                                            related_name="taggers")
    tagger_object_id = models.PositiveIntegerField()
    tagger_content_object = generic.GenericForeignKey("tagger_content_type",
                                                      "tagger_object_id")

    # The object that is tagged
    tagged_content_type = models.ForeignKey(ContentType,
                                            related_name="taggeds")
    tagged_object_id = models.PositiveIntegerField()
    tagged_content_object = generic.GenericForeignKey("tagged_content_type",
                                                      "tagged_object_id")

    # The object where the tagged objects is tagged
    tagged_in_content_type = models.ForeignKey(
        ContentType,
        related_name="tags")
    tagged_in_object_id = models.PositiveIntegerField()
    tagged_in_content_object = generic.GenericForeignKey(
        "tagged_in_content_type",
        "tagged_in_object_id")

    created_at = models.DateTimeField(auto_now_add=True)
    
    params = models.CharField(max_length =1024, null=True, blank=True)

    objects = PassThroughManager.for_queryset_class(O2OTagQuerySet)()

    class Meta:
        unique_together = ('tagger_content_type', 'tagger_object_id',
                           'tagged_content_type', 'tagged_object_id',
                           'tagged_in_content_type', 'tagged_in_object_id')

    def __unicode__(self):
        return u'%s -> %s | %s' % (self.tagger, self.tagged, self.tagged_in)

    # Convenient shortcuts
    @property
    def tagged(self):
        return self.tagged_content_object

    @property
    def tagger(self):
        return self.tagger_content_object

    @property
    def tagged_in(self):
        return self.tagged_in_content_object

    def get_item_new_tag_owner_context(self):
        tagger = self.tagger
        item = self.tagged_in
        tagged = self.tagged
        album = item.album
        if item.__class__._meta.object_name == "Picture":
            item_type = 1
        else:
            item_type = 2
        content = {
            'userId': str(tagger.id),
            'itemType': str(item_type),
            'itemId': str(item.id),
            'taggerName': tagger.get_full_name(),
            'userName': tagged.get_full_name(),
            'thumbUrl': item.image_thumb.url if item_type == 1 else item.thumb,
            'albumTitle': album.title or '',
            'albumId': str(album.id),
            'ios_type': 'APNS_TAG',
            'android_type': '27',
            'site_domain': 'eversnapapp.com'
        }
    
        return content

    def get_item_new_tag_context(self):
        tagger = self.tagger
        item = self.tagged_in
        tagged = self.tagged
        album = item.album
        if item.__class__._meta.object_name == "Picture":
            item_type = 1
        else:
            item_type = 2
        content = {
            'userId': str(tagger.id),
            'itemType': str(item_type),
            'itemId': str(item.id),
            'taggerName': tagger.get_full_name(),
            'thumbUrl': item.image_thumb.url if item_type == 1 else item.thumb,
            'userName': tagged.get_full_name(),
            'albumTitle': item.album.title or '',
            'albumId': str(item.album.id),
            'ios_type': 'APNS_TAG_TAGGED',
            'android_type': '31',
            'site_domain': 'eversnapapp.com'
        }
    
        return content
        
    @classmethod
    def get_notification_context(cls, notification_type, instance=None, objects=[]):
        if instance is not None:
            obj = instance
        else:
            obj = objects[0]
        method_name = "get_%s_context" % notification_type
        context = getattr(obj, method_name)()
        if instance is not None:
            return context
        object_count = len(objects)
        mob_index = min(object_count, 4)
        context['ios_type'] = settings.MOB_TYPES[notification_type][mob_index]['ios']
        context['android_type'] = settings.MOB_TYPES[notification_type][mob_index]['android']
        if object_count > 1:
            user = objects[1].tagged
            tagger = objects[1].tagger
            context["userName2"] = context["userName"]
            context["taggerName2"] = context["taggerName"]
            context["userName"] = (user.firstName or '') + (' ' + user.lastName if user.lastName else '')
            context["taggerName"] = tagger.get_full_name()
            last_item = getattr(objects[-1], method_name)()
            context["thumbUrl"] = last_item["thumbUrl"]
            context["itemId"] = last_item["itemId"]
        else:
            return context
        if object_count == 3:
            user = objects[2].tagged
            tagger = objects[2].tagger
            context["userName3"] = context["userName2"]
            context["userName2"] = context["userName"]
            context["taggerName3"] = context["taggerName2"]
            context["taggerName2"] = context["taggerName"]
            context["userName"] = (user.firstName or '') + (' ' + user.lastName if user.lastName else '')
            context["taggerName"] = tagger.get_full_name()
        elif object_count >2:
            user = objects[-2].tagged
            tagger = objects[-2].tagger
            context["userName2"] = (user.firstName or '') + (' ' + user.lastName if user.lastName else '')
            context["taggerName2"] = tagger.get_full_name()
            tagger = objects[-1].tagger
            user = objects[-1].tagged
            context["userName"] = (user.firstName or '') + (' ' + user.lastName if user.lastName else '')
            context["taggerName"] = tagger.get_full_name()
            context["totalUsers"] = object_count - 1
        # Remove same names if there are any    
        for base_key in ["taggerName%d", "userName%d"]:
            key3 = base_key % 3
            key2 = base_key % 2
            key1 = base_key.replace("%d", "")
            if key3 in context:
                if context[key3] in [context[key1], context[key2]]:
                    context.pop(key3)
            if key2 in context:
                if context[key2] == context[key1]:
                    if key3 in context:
                        context[key2] = context.pop(key3)
                    else:
                        context.pop(key2)
        return context
