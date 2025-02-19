from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

from app.datadase.models import ClientAuth
from app.datadase.dependencies import get_db

from .schemas import UserReg, UserMain, UserAuth

from app.api.auth.core.utils import hash_password, validate_password

router = APIRouter(prefix='/auth', tags = ['Auth'])

security = HTTPBasic

@router.get('/test')
def test():
    return {'message:': 'Test'}

@router.post('/reg', response_model=UserMain)
async def reg(client: UserReg, db: AsyncSession = Depends(get_db)):
    password = client.password # получаем пароль
    hashed_password = hash_password(password) # хэшируем пароль

    client_data = client.model_dump() # получаем словарь из модели
    client_data['password'] = hashed_password # заменяем пароль 
    db_client = ClientAuth(**client_data)
    db.add(db_client)
    try:
        await db.commit()
        await db.refresh(db_client)
        return UserMain.model_validate(db_client)
    except IntegrityError as e:
        print (str(e))
        await db.rollback()
        if 'unique constraint "clients_username_key"' in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"  # имя пользователя уже существует
            )
        elif 'unique constraint "clients_email_key"' in str(e):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists" # почта уже существует
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error"  
            )


@router.post('/auth', response_model=UserMain)
async def auth(client: UserAuth, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ClientAuth).where(client.email == ClientAuth.email)
    )
    db_client = result.scalars().first()
    if db_client is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    password = client.password
    if not validate_password(password, db_client.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return UserMain.model_validate(db_client)


