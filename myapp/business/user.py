from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from schema.token import TokenDataSchema, TokenSchema
from schema.user import UserCreateSchema, UserPassSchema, UserLoginSchema, UserTokenSchema, UserSchema, UserListSchema
from database.model.user import UserModel
from dependency.oauth import oauth2_scheme
from dependency.oauth import SECRET_KEY,ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from fastapi import Depends
from jose import JWTError, jwt
import bcrypt
import re


class UserBusiness:
    def __init__(self, db: Session):
        self.db = db

    async def user_get_all(self):
        """
        Lista todos os usuarios
        :return: lista de usuarios
        """
        user_list = []
        for user in self.db.query(UserModel).all():
            user_list.append(
                UserSchema(
                    username=user.username,
                    email=user.email
                )
            )
        return UserListSchema(users=user_list, total=self.db.query(UserModel).count())

    async def post_user(self, user_body: UserCreateSchema) -> UserModel:
        """
        Cadastra um novo usuario
        :param user_body: schema do pydantic
        :return: model de usuario
        """
        self._user_body_check(user_body)
        user = self._user_filter_email(user_body.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": {"user": "user already registered"}},
                headers={"X-Error": "body error"}
            )
        new_user = UserModel(username=user_body.username, email=user_body.email, password=self._password_hashed(user_body.password))
        self.db.add(new_user)
        self.db.commit()
        return new_user

    async def user_login(self, user_body: OAuth2PasswordRequestForm) -> TokenSchema:
        """
        Login de usuario
        :param user_body: schema de OAuth2PasswordRequestForm
        :return: token jwt
        """
        login_exception = HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"error": "username or password, incorrect"},
            headers={"X-Error": "body error"}
        )

        user = self.get_user(user_body.username)

        if not user:
            raise login_exception

        if not self._password_hashed_check(user_body.password, user.hashed_password):
            raise login_exception

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

        return TokenSchema(access_token=access_token)


    @staticmethod
    def _password_hashed(password: str) -> str:
        """
        Gera um hash
        :param password: passorwd do usuario
        :return: password hash
        """
        pwhash = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        return pwhash.decode('utf8')

    @staticmethod
    def _password_hashed_check(password: str, hash_pass: str) -> bool:
        """
        Verifica se o password e valido
        :param password: password do usuario
        :param hash_pass: password hash
        :return: boolean
        """
        return bcrypt.checkpw(password.encode('utf-8'), hash_pass.encode('utf-8'))

    def _user_filter_email(self, email: str):
        """
        Pesquisa usuario por email
        :param email: email do usuario
        :return: model de usuario
        """
        return self.db.query(UserModel).filter_by(email=email).first()

    @staticmethod
    def _user_body_check(user_body: UserCreateSchema):
        """
        Verifica se o json enviado atende as regras
        :param user_body: schema do pydantic
        :return: Nao retorna
        """
        detail_field = {}

        if user_body.password != user_body.confirm_password:
            detail_field["confirm_password"] = "confirm password different from password"

        if len(user_body.username) > 50 or len(user_body.username) < 5:
            detail_field["name"] = "name must have a maximum of 50 and a minimum of 5 digits."

        email = user_body.email.replace(" ", "")
        if len(email) > 60 or not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email):
            detail_field["email"] = "invalid email."

        if len(user_body.password) > 50 or len(user_body.password) < 8:
            detail_field["password"] = "password must have a maximum of 50 and a minimum of 8 digits."

        if user_body.password != user_body.confirm_password:
            detail_field["confirm_password"] = "password different from confirm_password"

        if detail_field:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": detail_field},
                headers={"X-Error": "body error"}
            )

    def get_user(self, username: str):
        """
        Pesquisa usuario por username
        :param username: username do usuario
        :return: schema do pydantic
        """
        user = self.db.query(UserModel).filter_by(username=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"error": "User not found"},
                headers={"X-Error": "body error"}
            )
        return UserPassSchema(
            username=user.username,
            email=user.email,
            hashed_password=user.password)

    # async def get_current_user(self, token: str = Depends(oauth2_scheme)):
    #     """
    #
    #     :param token:
    #     :return:
    #     """
    #     credentials_exception = HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Could not validate credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    #     try:
    #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    #         username: str = payload.get("sub")
    #         if username is None:
    #             raise credentials_exception
    #         token_data = TokenDataSchema(username=username)
    #     except JWTError:
    #         raise credentials_exception
    #     user = self.get_user(username=token_data.username)
    #     if user is None:
    #         raise credentials_exception
    #     return user
