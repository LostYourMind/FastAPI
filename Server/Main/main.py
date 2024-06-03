import logging
import sys
import os
import httpx
from typing import List, Dict, Optional

sys.path.append("../")  # 상위 디렉터리 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from DB.database_session import get_db
from DB.crud import call_select_all_kiosk


from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from pydantic import BaseModel

from API_CODE.DBControl.dbControl import get_db_control, dbControl
from API_CODE.Control.Main_Control import Control
from API_CODE.Module.PayMent import Payment_Class, PaymentRequest, PaymentResponse
from API_CODE.DataModel.DataModels import (
    Message,
    PaymentResponse,
    PaymentRequest,
    AddToCartRequest,
)

# region Instance


# FastAPI 앱 인스턴스를 생성
app = FastAPI()


# Main_Control.Control 인스턴스 생성
control_Instance = Control()


# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Uvicorn")

# 결제 기능이 있는 Spring Server URL
payment_processor = Payment_Class(client_url="http://spring-server-address")


# endregion

# region CORS 설정 코드

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 출처에서의 요청을 허용
    allow_credentials=False,  # 크로스 오리진 요청 시 쿠키를 지원
    allow_methods=["*"],  # 모든 HTTP 메소드를 허용
    allow_headers=["*"],  # 모든 헤더를 허용
)

# endregion

# region Server startup & shutdown Code


@app.on_event("startup")
async def startup():
    global db_connection
    try:
        with ThreadPoolExecutor() as executor:
            db_connection = executor.submit(next, get_db()).result()
        if not db_connection:
            raise HTTPException(status_code=500, detail="Database connection failed")
        logger.info("데이터베이스 연결이 성공적으로 시작되었습니다.")
    except Exception as e:
        logger.error(f"데이터베이스 연결 시작 실패: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")


@app.on_event("shutdown")
async def shutdown():
    global db_connection
    try:
        db_connection.close()
        logger.info("데이터베이스 연결이 성공적으로 종료되었습니다.")
    except Exception as e:
        logger.error(f"데이터베이스 연결 종료 실패: {e}")


# endregion


@app.post("/users/ai")
async def get_products(
    message: Message, db_control: dbControl = Depends(get_db_control)
):
    logger.info(
        f"KioskID {message.id_Value} text {message.text} sender {message.sender}"
    )
    logger.info(f"/users/ai : Post Request Start\n")
    logger.info(f"KioskID : {message.id_Value} \nMessage : {message.text}")

    # KioskID를 가지고 해당 가게 키오스크 메뉴 정보 추출 후 문장 생성
    try:
        logger.info("Get Product Start...")
        products = db_control.select_product(message.id_Value)
        if products is None:
            raise HTTPException(status_code=500, detail="Failed to fetch products")
        logger.info(f"Product List : {products}")
        result = control_Instance.Control_SrInput(
            message.text, products, message.id_Value
        )
        if isinstance(result, str):
            logger.info(f"/user/ai : {result}")
            return {"message": result}
        else:
            raise ValueError("Unexpected response format")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    #return {"message": message.text}  # ECHO용 코드


# 장바구니에 아이템을 추가하는 엔드포인트
@app.post("/users/addToCart")
async def add_to_cart(request: AddToCartRequest, db_control=Depends(get_db_control)):
    logger.info("/users/addToCart")
    user_id = request.user_id
    items = request.items

    product_List = db_control.select_product(request.user_id)

    result = control_Instance.Add_WishList(user_id, items, product_List)
    logger.info(f"result value : {result}")
    if result == None:
        raise HTTPException(status_code=404, detail=f"Product {items} not found")
    else:
        return result


# 결제 기능을 위한 엔드포인트
@app.post("/users/paymentAPI")
async def handle_payment_request(request: PaymentRequest):
    if not request.paymentData:
        raise HTTPException(status_code=400, detail="Payment data is missing")

    payment_data = request.paymentData
    return await payment_processor.process_payment(
        user_id=request.user_id,
        cart_data=payment_data.get("items"),
        total_amount=payment_data.get("total_amount"),
        item_name=payment_data.get("item_name"),
        quantity=payment_data.get("quantity"),
    )
