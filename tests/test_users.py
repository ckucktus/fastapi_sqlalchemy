from httpx import AsyncClient
import pytest
from sql_app.crud import Users_CRUD
from main import app
from core.security import create_access_token

pytestmark = pytest.mark.asyncio






class TestCreateUser:
    json = {
    "name": "test",
    "email": "test@mail.ru",
    "is_company": True,
    "password": "stringst",
    "password2": "stringst"
    }

    async def test_check_create_user(self, client:AsyncClient, db):
        
        response = await client.post(app.url_path_for('create_user'), 
            json=self.json
        )
        assert response.status_code == 200
        assert not response.json().get('password')
        email = response.json().get('email')
        user = await Users_CRUD.get_by_email(email, db)
        await db.delete(user)

class TestUpdateUser:
    json = {
    "name": "test",
    "email": "test@mail.ru",
    "is_company": True,
    "password": "stringst",
    "password2": "stringst"
    }
    update_json = {
    "name": "updated_name",
    "email": "test@mail.ru",
    "is_company": True,
    "password": "stringst",
    "password2": "stringst"
    }
    async def test_update_user_with_token(self, client:AsyncClient, create_user, db):
        # user = await Users_CRUD.create(UserIn.parse_obj(self.json), db)
        # await db.commit()
        token = create_access_token({"sub": str(create_user.id)})
        headers = {
            'accept': 'application/json',
            'Authorization' : f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = await client.put(app.url_path_for('update_user'), 
            headers = headers,
            json=self.update_json
        )
        assert response.status_code == 200
        await db.delete(create_user)

    async def test_update_user_without_token(self, client:AsyncClient, db):
        response = await client.put(app.url_path_for('update_user'), 
            json=self.update_json
        )
        assert response.status_code == 403

class TestGetUserById:
    @pytest.mark.parametrize(
        "pk, status",[(0, 404), (2,200), (5, 404), (99999, 404), (-1, 422)]
    )
    async def test_get_by_id(self, client:AsyncClient, pk:int, status:int):
        response = await client.get(app.url_path_for('get_user_by_id'), 
            params={'pk': pk}
        )
        assert response.status_code == status

class TestGetListUsers:
    @pytest.mark.parametrize("offset, limit, status", (
        (0, 2, 200),
        (2, 0, 404),
        (2, 2, 200),
        (9999999, 2, 404),
        (-1, 2, 422),
        (-1, -2, 422)
    ))
    async def test_get_list_users(self, client:AsyncClient, offset:int, limit:int, status:int):
        response = await client.get(app.url_path_for('show_users'), 
            params={'offset': offset, 'limit':limit}
        )
        assert response.status_code == status
        if status == 200:
            len(response.json()) == limit
