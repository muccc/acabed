from django.db import models
from acab.models import AnimationInstance

# Create your models here.

ITEM_TYPE_MOVIE = 'm'
ITEM_TYPE_LOCAL_STREAM = 'l'
ITEM_TYPE_EXTERNAL_STREAM = 'e'
ITEM_TYPE_NOTHING = 'n'

HISTORY_CHOICES =((ITEM_TYPE_MOVIE, "MOVIE"),
                  (ITEM_TYPE_LOCAL_STREAM, "LOCAL"),
                  (ITEM_TYPE_EXTERNAL_STREAM, "EXTERNAL"),
                  (ITEM_TYPE_NOTHING, "NOTHING"))

STREAM_NEW = 'n'
STREAM_DENIED = 'd'
STREAM_ALLOWED = 'a'
STREAM_PLAYING = 'p'
STREAM_FINISHED = 'f'
STREAM_ERROR = 'e'

STREAM_CHOICES =((STREAM_NEW, "NEW"),
                  (STREAM_DENIED, "DENIED"),
                  (STREAM_ALLOWED, "ALLOWED"),
                  (STREAM_PLAYING, "PLAYING"),
                  (STREAM_FINISHED, "FINISHED"),
                  (STREAM_ERROR, "ERROR"))

class HistoryManager(models.Manager):
    def get_latest(self):
        try:
            latest = self.all().latest()
        except History.DoesNotExist:
            latest = History(type = ITEM_TYPE_NOTHING,
                             title = "Nothing yet")
            latest.save()
        return latest
     
    def push_movie(self, ai):
        new = History(type = ITEM_TYPE_MOVIE,
                      title = ai.animation.title,
                      description = ai.animation.description,
                      author = ai.animation.author,
                      animationInstance = ai)
        
        new.save()
        self.trim()
        
    def trim(self):
        """Delete all but the newest 100"""
        for h in self.all()[100:]:
            h.delete()

class History(models.Model):
    type = models.CharField(max_length=1, choices=HISTORY_CHOICES)
    title = models.CharField(max_length=128)
    description = models.TextField()
    author = models.CharField(max_length=512)
    played = models.DateTimeField(auto_now_add = True)
    animationInstance = models.ForeignKey(AnimationInstance, blank=True, null=True)

    objects = HistoryManager()
    
    class Meta():
        get_latest_by = 'played'
        ordering = ['-played']
        
    def __unicode__(self):
        return "%s:%s, %s"%(self.type, self.title, self.played)

class StreamManager(models.Manager):
    def get_new_request(self):
        try:
            return self.get(state = STREAM_NEW)
        except StreamRequest.DoesNotExist:
            return self.get_empty_query_set()
    
    def restore(self):
        try:
            latest = self.latest()
            if latest.state == STREAM_NEW or latest.state == STREAM_ALLOWED or latest.state == STREAM_PLAYING:
                latest.state = STREAM_ERROR
                latest.save()
        except StreamRequest.DoesNotExist:
            pass
            
    #def push_new_request(self):
        #if not (self.filter(state=STREAM_NEW).exists() and 
        #        self.filter(state=STREAM_ALLOWED).exists() and 
        #        self.filter(state=STREAM_PLAYING).exists()):
        #    return StreamRequest(state=STREAM_NEW)
        #else:
        #    print "NONO"
        #    return None
        
        
class StreamRequest(models.Model):
    title = models.CharField(max_length=128, blank = True)
    author = models.CharField(max_length=512, blank = True)
    request_date = models.DateTimeField(auto_now_add = True)
    response_date = models.DateTimeField(blank = True, null = True)
    state = models.CharField(max_length=1, choices=STREAM_CHOICES) 
    
    objects = StreamManager()
    
    @staticmethod
    def push_new_request():
        if StreamRequest.objects.all().exists():
            latest = StreamRequest.objects.latest()
            if latest.state == STREAM_NEW or latest.state == STREAM_ALLOWED or latest.state == STREAM_PLAYING:
                return None
        
        r=StreamRequest(state=STREAM_NEW)
        r.save()
        return r
    
    class Meta():
        get_latest_by = 'request_date'
        ordering = ['-request_date']
        
    def __unicode__(self):
        return "%s @ %s (%s)"%(self.title, self.request_date, self.state)