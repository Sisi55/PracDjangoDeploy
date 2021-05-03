import csv
import json
import re
import collections
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

score = {
    'cart-create': 3,
    'order-create': 5,
    'click': 2,
    'hover': 1,
    'order-cancel': -6,
    'cart-cancel': -4,

    'cart-modify-plus': 3,
    'cart-modify-minus': -3,
}
size = 12

product_id_list_const = [3897, 3921, 3940, 3963,
                         3989, 4002, 4019, 4037,
                         4056, 4083, 4108, 4129,
                         4152, 4178, 4202, 4222,
                         4241, 4263, 4275, 4289, ]


def cf_result(es_response, request_body):
    columns = list(es_response[0].keys()) + ['actionType_score']

    columns_value_list = []

    for row in es_response:

        # 왼쪽부터 순차적으로 검사하나보다
        if str(row['userId']).isdigit() and str(row['productId']).isdigit() and 'categoryId' in row and str(
                row['categoryId']).isdigit():
            row['userId'] = int(row['userId'])
            row['productId'] = int(row['productId'])
            row['categoryId'] = int(row['categoryId'])

            if row['actionType'] in score:
                row['actionType_score'] = score[row['actionType']]
            else:
                row['actionType_score'] = 0

            columns_value_list.append(list(row.values()))

    base_df = pd.DataFrame(columns_value_list, columns=columns)

    w_actionType_df = base_df[['userId', 'productId', 'actionType_score']]

    actionType_matrix_itemCF = w_actionType_df.pivot_table('actionType_score', index='userId', columns='productId')
    actionType_matrix_itemCF = actionType_matrix_itemCF.fillna(0)

    actionType_matrix_userCF = w_actionType_df.pivot_table('actionType_score', index='productId', columns='userId')
    actionType_matrix_userCF = actionType_matrix_userCF.fillna(0)

    # itemId - itemId list
    item_similarity = cosine_similarity(actionType_matrix_userCF)
    item_sim_df = pd.DataFrame(data=item_similarity, index=actionType_matrix_userCF.index,
                               columns=actionType_matrix_userCF.index)  # 행으로 연산하는거 맞다
    # 루프 돌면서 : itemId
    item_cf_dict = {}
    for item_id in request_body['requestProductIdList']:
        if item_id in item_sim_df:
            item_cf_item_list = list(item_sim_df[item_id].sort_values(ascending=False)[1:1 + size].index)
            item_cf_dict[item_id] = item_cf_item_list
        else:
            item_cf_dict[item_id] = product_id_list_const

            # userId - userId[0] - itemId
    # 루프 돌면서 : userId requestUserIdList

    # 루프 돌면서 : itemId
    user_cf_dict = {}
    for user_id in request_body['requestUserIdList']:
        if user_id in actionType_matrix_userCF:
            sim_userId = \
            actionType_matrix_userCF.corrwith(actionType_matrix_userCF[user_id]).sort_values(ascending=False).index[1]
            mid_itemId = actionType_matrix_userCF[sim_userId].sort_values(ascending=False).index[0]

            user_cf_item_list = list(item_sim_df[mid_itemId].sort_values(ascending=False)[1:1 + size].index)
            user_cf_dict[user_id] = user_cf_item_list
        else:
            user_cf_dict[user_id] = product_id_list_const

    return {
        'itemCF': item_cf_dict,
        'userCF': user_cf_dict,
    }
