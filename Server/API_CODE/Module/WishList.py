#WishList.py

from typing import List, Dict
from API_CODE.DataModel.DataModels import CartItem


# 메모리에 장바구니 데이터를 저장할 딕셔너리
cart_data: Dict[int, List[str]] = {}


class WishList():

    def checkWishlist(self, user_id, items, product_List):

            # 사용자 ID에 대한 장바구니가 없으면 새로 생성
        if user_id not in cart_data:
            cart_data[user_id] = []

        added_items = []
        for item_name in items:
            product = next((product for product in product_List if product["product_name"] == item_name), None)
            if product:
                cart_item = CartItem(product_name=product["product_name"], price=product["price"])
                cart_data[user_id].append(cart_item)
                added_items.append(cart_item)
            else:
                return None

        return {
            "message": f"{', '.join([item.product_name for item in added_items])} 이(가) 장바구니에 추가되었습니다.",
            "items": added_items
    }
    
