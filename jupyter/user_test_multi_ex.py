from time import time
from urllib.request import Request, urlopen
import asyncio

import random
import csv
from selenium import webdriver
import os

import django

from cf_app.models import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings')
django.setup()


def get_product_id_list():
    result = []
    id_list = Product.objects.all().values('product_id')
    for row in id_list:
        result.append(row['product_id'])
    print(result)

    return result


product_id_list = get_product_id_list()

action_select_list = [0, 1]  # 0:장바구니 , 1:즉시주문


async def fetch():
    browser = webdriver.Chrome(executable_path='D:/000UbicFinal/chromedriver')

    while True:
        product_detail_id = random.choice(product_id_list)
        print(product_detail_id, browser, time())
        url_product_detail = 'http://localhost:8080/products/' + str(product_detail_id)
        browser.get(url_product_detail)  # 상품 상세 화면 이동

        # 장바구니 또는 바로구매
        action_flag = random.choice(action_select_list)
        if action_flag == 0:  # 장바구니
            print('장바구니 ', browser)
            browser.find_element_by_css_selector("button.btn.btn-primary.btn-lg.btn-shoplist").click()
        else:  # 즉시구매
            print('즉시구매 ', browser)
            browser.find_element_by_css_selector(
                "button.btn.btn-primary.btn-lg.btn-order-immediately-from-detail").click()

        await asyncio.sleep(3.0)  # 실전은 3초 대기. asyncio.sleep도 네이티브 코루틴


async def main():
    futures = [asyncio.ensure_future(fetch()) for test in range(5)]  # 10개 원소 리스트
    # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)  # 결과를 한꺼번에 가져옴 : 리스트 반환
    print(result)


begin = time()
loop = asyncio.get_event_loop()  # 이벤트 루프를 얻음
loop.run_until_complete(main())  # main이 끝날 때까지 기다림
loop.close()  # 이벤트 루프를 닫음
end = time()
print('실행 시간: {0:.3f}초'.format(end - begin))
