import copy
import json
import uuid

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from stock.views.vo.response import Response
from .request import StockOrder

"""
post 请求单元测试参数为
token 可能过期，使用自己的token
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTVlY
{
  "moneyType":2,
  "exchangeType":0,
  "entrustProp":"e",
  "requestId":"462731244548191027",
  "amountPerHand":2000,
  "stockCode":"00828",
  "stockName":"王朝酒业",
  "forceEntrustFlag":true,
  "entrustPrice":"0.320",
  "entrustAmount":2000,
  "marketStockType":10104,
  "entrustType":0
}
"""


@csrf_exempt
def stock_add_order(request):
    dict_stock_request = {}
    list_stock_response = []

    received_json_data = json.loads(request.body)
    dict_stock_request['stockCode'] = received_json_data.get('stockCode')
    dict_stock_request['stockName'] = received_json_data.get('stockName')
    dict_stock_request['entrustAmount'] = received_json_data.get('entrustAmount')
    dict_stock_request['entrustPrice'] = received_json_data.get('entrustPrice')
    dict_stock_request['entrustProp'] = received_json_data.get('entrustProp')
    dict_stock_request['entrustType'] = received_json_data.get('entrustType')
    dict_stock_request['exchangeType'] = received_json_data.get('exchangeType')
    dict_stock_request['forceEntrustFlag'] = True
    stock_order = StockOrder.stock_order(**dict_stock_request)
    headers = {'X-Lang': '1', 'X-Typ': '1',
               'Authorization': request.META.get('HTTP_AUTHORIZATION'),
               'Content-Type': 'application/json;charset=UTF-8', 'X-Dt': 't2'}

    # 正常的请求（所有的条件都通过）
    dict_stock_request['requestId'] = uuid.uuid1().hex
    r_normal = requests.post(url='https://jy1-sit.yxzq.com/stock-order-server/api/entrust-order/v1/',
                             json=dict_stock_request,
                             headers=headers)
    if json.loads(str(r_normal.content, 'utf-8')).get('code') != 0:
        return HttpResponse(
            Response.succeed('请保证当前的参数可以正常的请求通过，单元测试才会根据各个指标进行测试，当前失败原因为') + (
                json.loads(str(r_normal.content, 'utf-8')).get('msg')))

    # 委托参数缺失
    for k, v in dict_stock_request.items():
        this_result = ''
        dict_stock_request['requestId'] = uuid.uuid1().hex
        dict_stock_not_param = copy.deepcopy(dict_stock_request)
        dict_stock_not_param.pop(k)
        r_not_price = requests.post(url='https://jy1-sit.yxzq.com/stock-order-server/api/entrust-order/v1/',
                                    json=dict_stock_not_param,
                                    headers=headers)
        if json.loads(str(r_not_price.content, 'utf-8')).get('code') != 0:
            this_result = this_result + (k + ('缺失响应报文\n') + (str(r_not_price.content, 'utf-8')) + ('\n测试通过'))
        else:
            this_result = this_result + (k + ('缺失响应报文\n') + (str(r_not_price.content, 'utf-8')) + ('\n测试不通过'))
        list_stock_response.append(this_result)

    # 3000手限制，委托属性限制，竞价单不能输入价格，检查9档24价格检查
    for k, v in dict_stock_request.items():
        dict_stock_request['requestId'] = uuid.uuid1().hex
        dict_stock_error_param = copy.deepcopy(dict_stock_request)

        this_result = ''
        # 3000手限制
        if k == 'entrustAmount':
            dict_stock_error_param[k] = 9999999999
            r_3000_result = requests.post(url='https://jy1-sit.yxzq.com/stock-order-server/api/entrust-order/v1/',
                                          json=dict_stock_error_param,
                                          headers=headers)
            if json.loads(str(r_3000_result.content, 'utf-8')).get('code') != 0:
                this_result = this_result + ('3000手验证结果\n' + (str(r_3000_result.content, 'utf-8')) + ('\n测试通过'))
            else:
                this_result = this_result + ('3000手验证结果\n' + (str(r_3000_result.content, 'utf-8')) + ('\n测试不通过'))
        # 委托属性限制
        elif k == 'entrustProp':
            dict_stock_error_param[k] = 'asd'
            r_entrust_prop = requests.post(url='https://jy1-sit.yxzq.com/stock-order-server/api/entrust-order/v1/',
                                           json=dict_stock_error_param,
                                           headers=headers)
            if json.loads(str(r_entrust_prop.content, 'utf-8')).get('code') != 0:
                this_result = this_result + ('委托属性限制结果\n' + (str(r_entrust_prop.content, 'utf-8')) + ('\n测试通过'))
            else:
                this_result = this_result + ('委托属性限制结果\n' + (str(r_entrust_prop.content, 'utf-8')) + ('\n测试不通过'))
        # 检查9档24价格检查
        elif k == 'entrustPrice':
            dict_stock_error_param['entrustPrice'] = 9999999
            dict_stock_error_param['forceEntrustFlag'] = False
            r_entrust_price = requests.post(url='http://127.0.0.1:9903/stock-order-server/api/entrust-order/v1/',
                                            json=dict_stock_error_param,
                                            headers=headers)
            if json.loads(str(r_entrust_price.content, 'utf-8')).get('code') != 0:
                this_result = this_result + ('检查9档24价格检查结果\n' + (str(r_entrust_price.content, 'utf-8')) + ('\n测试通过'))
            else:
                this_result = this_result + ('检查9档24价格检查结果\n' + (str(r_entrust_price.content, 'utf-8')) + ('\n测试不通过'))

        if this_result != '':
            list_stock_response.append(this_result)

    # 竞价单不能输入价格
    if stock_order.entrustProp == 'd':
        this_result = ''
        dict_stock_request['requestId'] = uuid.uuid1().hex
        dict_stock_request['entrustPrice'] = '0'
        dict_order_price_d = copy.deepcopy(dict_stock_request)
        r_entrust_price_d = requests.post(url='https://jy1-sit.yxzq.com/stock-order-server/api/entrust-order/v1/',
                                          json=dict_order_price_d,
                                          headers=headers)
        if json.loads(str(r_entrust_price_d.content, 'utf-8')).get('code') != 0:
            this_result = this_result + ('竞价单不能输入价格结果\n' + (str(r_entrust_price_d.content, 'utf-8')) + ('\n测试通过'))
        else:
            this_result = this_result + ('竞价单不能输入价格结果\n' + (str(r_entrust_price_d.content, 'utf-8')) + ('\n测试不通过'))
        list_stock_response.append(this_result)

    print(list_stock_response)
    return HttpResponse(Response.succeed(list_stock_response))
