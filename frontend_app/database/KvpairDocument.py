from mongoengine import Document, StringField
from models.kvpair import Kvpair


class KvpairDocument(Document):
    key = StringField(required=True, unique=True)
    value = StringField(required=True)
    meta = {
        'collection': 'kvpairs',
        'indexes': ['key'],
    }

    @classmethod
    def from_kvpair(cls, kvpair: Kvpair):
        return cls(**vars(kvpair))

    def to_kvpair(self) -> Kvpair:
        doc_dict = self.to_mongo().to_dict()
        doc_dict.pop('_id')
        return Kvpair(**doc_dict)
