from fastapi import HTTPException
import httpx
from pydantic import BaseModel


class Payment_Class:
    def __init__(self, client_url):
        self.client_url = client_url

    async def process_payment(
        self,
        user_id: int,
        cart_data: dict,
        total_amount: int,
        item_name: str,
        quantity: int,
    ):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.client_url}/pay",
                    json={
                        "user_id": user_id,
                        "total_amount": total_amount,
                        "items": cart_data,
                        "item_name": item_name,
                        "quantity": quantity,
                    },
                )
                response_data = response.json()

                if response.status_code == 200 and response_data.get("success"):
                    cart_data.clear()
                    return PaymentResponse(
                        message="결제가 성공적으로 완료되었습니다.",
                        success=True,
                        total_amount=total_amount,
                    )
                else:
                    raise HTTPException(status_code=400, detail="Payment failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
