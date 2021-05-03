import collections

import urllib3
import json
import pickle
import pandas as pd

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from cf_app.utils import cf_result
from config import settings


@api_view(['GET'])
def test_api(request):
    return Response({"message": "ok."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_es_list_api(request):
    """
    http://127.0.0.1:8000/cf/es-list/?index_name=ubic_click_action&action_type=order
    """
    index_name = request.query_params.get('index_name')
    actionType = request.query_params.get('action_type')

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match": {
            "actionType": actionType
        }}}  # _all
    )["count"]
    print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match": {  # _all
                    "actionType": actionType
                }
            }
        },
        size=size,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )
    # print(response)

    result = get_pretty_response(response)

    ''' 결과 배열의 원소 모양 : 자바에서 바로 클래스 배열로 받으면 된다
        {
            "now": "2020-09-10T16:53:51.114428",
            "userId": "47161",
            "productId": 20522,
            "categoryId": 18,
            "actionType": "order"
        },
    '''
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])  # userId 가 필요하네 !
def get_last50_for_category_score_from_ES(request):
    """
        엘라스틱서치에서 최근 50개 행동 가져와서 category_score 로 변경하는 함수
        http://127.0.0.1:8000/cf/category-score/?index_name=ubic_click_action&user_id=47161
    """
    index_name = request.query_params.get('index_name')
    user_id = request.query_params.get('user_id')

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match": {
            "userId": user_id
        }}}  # _all
    )["count"]
    print('size', size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match": {  # _all
                    "userId": user_id
                }
            }
        },
        size=size,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )
    # print(response)

    # category_score 계산 로직
    try:
        response = get_pretty_response(response)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    category_score = collections.defaultdict(int)
    for action in response:  #
        # print(action['actionType'])
        if action['actionType'] == 'hover':
            category_score[action['categoryId']] += 1
        elif action['actionType'] == 'click':
            category_score[action['categoryId']] += 3
        elif action['actionType'] == 'cart-create':
            category_score[action['categoryId']] += 5
        elif action['actionType'] == 'order-create':
            category_score[action['categoryId']] += 7

    # 근데 사실 필요한건 가장 점수가 높은 카테고리 값!
    def return_value_from_dict(x):
        return x[1]

    # print('정렬전 ', category_score)
    result = sorted(category_score.items(), key=return_value_from_dict, reverse=True)
    print('정렬후 ', result)
    # result[0][0] # category:score 니까 [0]

    # result = []
    return Response({
        'maxScoreCategory': result[0][0]
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_all_es_data(request):
    """
    elastic search 모든 데이터 가져와서 userCF 연산 적용한다
    """
    index_name = 'ubic_click_action'

    client = Elasticsearch(settings.ES_SECRET_KEY)

    size = client.count(
        index=index_name,
        body={'query': {"match_all": {
        }}}  # _all
    )["count"]
    print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match_all": {  # _all
                }
            }
        },
        size=10000,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )

    try:
        response = get_pretty_response(response)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    return Response(response
                    , status=status.HTTP_200_OK)


@api_view(['POST'])
def get_cf(request):
    """
    elastic search 모든 데이터 가져와서 userCF 연산 적용한다
    """
    # print(request.body)
    request_body = json.loads(request.body)
    # print(request_body)

    index_name = 'ubic_click_action'

    client = Elasticsearch(settings.ES_SECRET_KEY)

    # size = client.count(
    #     index=index_name,
    #     body={'query': {"match_all": {
    #     }}}  # _all
    # )["count"]
    # # print(size)

    response = client.search(
        index=index_name,
        body={
            "query": {
                "match_all": {  # _all
                }
            }
        },
        size=10000,
        filter_path=['hits.hits._source']  # 이 아래 내용만 나온다는건데 별로 필요없음
    )

    try:
        response = get_pretty_response(response)
    except:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    # CF 연산
    cf_result_dict = cf_result(response, request_body)
    # .pkl 저장
    with open('list.pkl', 'rb') as f:
        existing_data = pickle.load(f)

    with open('list.pkl', 'wb') as f:
        # 기존 값에 덮어쓰기
        existing_data['itemCF'].update(cf_result_dict['itemCF'])
        existing_data['userCF'].update(cf_result_dict['userCF'])
        pickle.dump(existing_data, f)

    return Response(cf_result_dict, status=status.HTTP_200_OK)


def get_pretty_response(response):
    """
    elastic search data 파싱 작업 함수
    """
    response = response['hits']['hits']  # list : filter_path
    # df = pd.DataFrame(response)

    # response 루프돌면서 _source 의 값들의 배열로 만들거야
    result = []
    for row in response:
        row = row['_source']
        result.append(row)

    return result


# def search_test():
@api_view(['GET'])
def test_es_get_all_api(request):
    http = urllib3.PoolManager()

    index_name = request.query_params.get('index_name')
    ES_INDEX_SIZE_URL = settings.ES_SECRET_KEY + f'/_cat/count/{index_name}'  # 실패
    print(ES_INDEX_SIZE_URL)
    response = http.request(
        "GET",
        ES_INDEX_SIZE_URL,
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body={}
    )
    print("[responseCode] " + str(response.status))
    # Decode UTF-8 bytes to Unicode, and convert single quotes
    response = response.data.decode('utf8').replace("'", '"')
    # Load the JSON to a Python list
    response = json.loads(response)
    print("[response] " + str(response))

    return Response({"message": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api1(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api2(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api3(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api4(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api5(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_get_productIdList_api6(request):
    response = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    return Response({"productIdList": response}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_write_pkl_api(request):
    productIdList = [3897, 3921, 3940, 3963, 3989, 4002, 4019, 4037,
                     4056, 4083, 4108, 4129, 4152, 4178, 4202, 4222]
    with open('list.pkl', 'wb') as f:
        pickle.dump(productIdList, f)

    return Response({}, status=status.HTTP_200_OK)


@api_view(['GET'])
def test_read_pkl_api(request):
    with open('list.pkl', 'rb') as f:
        data = pickle.load(f)
    print(data)
    return Response({"message": data}, status=status.HTTP_200_OK)
