import os
import sys
import logging
from fastapi import Depends
from sqlalchemy.orm import Session

# 로그 설정
logger = logging.getLogger("DBControl")

# 현재 파일의 디렉토리를 모듈 검색 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 필요한 모듈 임포트
from DB.database_session import get_db
from DB.crud import call_select_all_kiosk

class dbControl:

    def __init__(self, db: Session):
        self.db = db

    def select_product(self, user_id):
        logger.info("Run : select_Product")
        try:
            result = call_select_all_kiosk(self.db, user_id)
            keys = ['userId', 'user_name', 'kioskId', 'storeName', 'categoryName', 'product_name', 'price', 'image']

            products = [
                {"product_name": dict(zip(keys, row)).get("product_name"),
                 "price": dict(zip(keys, row)).get("price")}
                for row in result
            ]

            return products
        except Exception as e:
            logger.error(f"Failed to fetch products: {e}")
            return None


# FastAPI 의존성 주입 함수
def get_db_control(db: Session = Depends(get_db)):
    return dbControl(db)
