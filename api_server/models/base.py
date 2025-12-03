import mongoengine
from utils.counters import get_next_sequence

class BaseDocument(mongoengine.Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }
    
    id = mongoengine.IntField(primary_key=True)
    
    def save(self, *args, **kwargs):
        if getattr(self, 'id', None) is None:
            collection_name = getattr(self, 'meta', {}).get('collection',
                                                            self.__class__.__name__.lower())
            self.id = get_next_sequence(collection_name)
        return super(BaseDocument, self).save(*args, **kwargs)