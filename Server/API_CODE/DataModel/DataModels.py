from pydantic import BaseModel
from typing import List, Dict, Optional

# AI 기능 메세지 데이터 모델
class Message(BaseModel):
    text: str
    sender: str
    id_Value: int
    paymentData: Optional[dict] = None


# 결제 응답 데이터 모델
class PaymentResponse(BaseModel):
    message: str
    success: bool
    total_amount: int = 0

# 결제 요청 데이터 모델
class PaymentRequest(BaseModel):
    user_id: int
    action: str
    paymentData: dict = None

# 장바구니 담기 요청 데이터 모델
class AddToCartRequest(BaseModel):
    user_id: int
    items: List[str]

# 장바구니 데이터 모델
class CartItem(BaseModel):
    product_name: str
    price: int