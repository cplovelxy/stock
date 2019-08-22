from datetime import datetime

from django.db import transaction
from django.forms.models import model_to_dict
from django.http import HttpResponse

from stock.views.vo.response import Response
from stock.models import Order


@transaction.atomic
def db_message(request):
    order_object = Order(user_id=111, order_no='111', order_price=0.35, create_time=datetime.now(),
                         update_time=datetime.now())
    order_object.save()
    obj = model_to_dict(order_object)

    return HttpResponse(Response.succeed(obj))
