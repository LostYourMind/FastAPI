# Main_Control.py
# Module에 있는 코드를 사용하기 위한 호출 담당

import sys
sys.path.append("../")  # 상위 디렉터리 추가

from API_CODE.Module import GPT_API
from API_CODE.Module.WishList import WishList


class Control:

    # 음성 인식처리 & 추천 기능 함수 호출
    def Control_SrInput(self, text, products, id_Value):
        keyword = "예산"
        temp = text

        # 조건 리스트 정의
        explanations = ["설명해 줘", "설명해 줘.", "알려 줘", "설명해 주세요"]
        recommendations = ["추천해 줘", "추천해 줘.", "추천해 주세요", "추천 바래"]

        # 설명 관련 조건 처리
        if any(temp.endswith(phrase) for phrase in explanations):
            call_GPT = Control.Call_Generate_Sentences(self, temp)
            return call_GPT

        # 추천 관련 조건 처리
        elif any(temp.endswith(phrase) for phrase in recommendations):
            allergy_Info = "계란"
            call_GPT = Control.recom_Function(self, allergy_Info, products)
            return call_GPT

        # 예산 관련 조건 처리
        elif keyword in temp:
            call_GPT = Control.recom_Function_Budget(self, temp, products)
            return call_GPT

        # 기타 조건 처리
        else:
            return "테스트"


    # 추천 기능 호출 함수
    def recom_Function(self, allergy, products):
        allergy_Info = ""
        if allergy.endswith("알레르기"):
            allergy_Info = allergy
        else:
            temp = [allergy, "알레르기"]
            allergy_Info = " ".join(temp)

        call_GPT = GPT_API.USE_GPT()
        return_value = call_GPT.Recomm_Menu(allergy_Info, products)
        return return_value

    # 예산 기반 추천
    def recom_Function_Budget(self, temp, products):
        call_GPT = GPT_API.USE_GPT()
        return_value = call_GPT.Recomm_Menu(temp, products)
        return return_value

    # 답변 생성 기능 호출 함수
    def Call_Generate_Sentences(self, prompt):
        call_GPT = GPT_API.USE_GPT()
        result_value = call_GPT.generate_Sentences(prompt)
        return result_value

    # 장바구니 추가 기능
    def Add_WishList(self, user_id, items, product_List):
        wishlist = WishList.checkWishlist(self, user_id, items, product_List)
        return wishlist
