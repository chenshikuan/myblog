from django.contrib.contenttypes.models import ContentType
from .models import ReadNum


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.id)
    if not request.COOKIES.get(key):

        if ReadNum.objects.filter(content_type=ct, object_id=obj.id).count():
            readnum = ReadNum.objects.get(content_type=ct, object_id=obj.id)
        else:
            readnum = ReadNum(content_type=ct, object_id=obj.id)
        readnum.read_num += 1
        readnum.save()
    return key