import json
from datetime import datetime

from django.http import HttpResponse

from .vo.response import Response
from ..models import Order


def db_message(request):
    order_object = Order(user_id=111, order_no='111', order_price=0.35, create_time=datetime.now(),
                         update_time=datetime.now())
    order_object.save()
    return HttpResponse(Response.succeed(body=json.dumps(order_object.__dict__, ensure_ascii=False)))
