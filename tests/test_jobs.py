from httpx import AsyncClient
import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from sql_app.crud import Jobs_CRUD, Users_CRUD
from main import app
from core.security import create_access_token

from sql_app.models import Jobs, Users

pytestmark = pytest.mark.asyncio

class TestGetListJobs:
    @pytest.mark.parametrize("offset, limit, status", (
        (0, 2, 200),
        (2, 0, 404),
        (2, 2, 200),
        (9999999, 2, 404),
        (-1, 2, 422),
        (-1, -2, 422)
    ))
    async def test_get_list_jobs(self, client:AsyncClient, offset:int, limit:int, status:int):
        response = await client.get(app.url_path_for('get_list_jobs'), 
            params={'offset': offset, 'limit':limit}
        )
        assert response.status_code == status
        if status == 200:
            len(response.json()) == limit

class TestGetJobById:
    @pytest.mark.parametrize(
        "pk, status",[(0, 404), (2,200), (5, 404), (99999, 404), (-1, 422)]
    )
    async def test_get_by_id(self, client:AsyncClient, pk:int, status:int):
        response = await client.get(app.url_path_for('get_user_by_id'), 
            params={'pk': pk}
        )
        assert response.status_code == status

class TestCreateJobs:
    json = {
    "title": "Software Engineer",
    "description": "string",
    "salary_from": 1000,
    "salary_to": 5000,
    "is_active": True
    }

    async def test_check_create_user_with_permissons(self, client:AsyncClient, create_company:Users, db:AsyncSession):
        token = create_access_token({"sub": str(create_company.id)})
        headers = {
            'accept': 'application/json',
            'Authorization' : f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = await client.post(app.url_path_for('create_job'), 
            json=self.json,
            headers=headers
        )
        assert response.status_code == 200
        pk = response.json().get('id')
        job = await Jobs_CRUD.get_job_by_id(pk, db)
        await db.delete(job)
        await db.delete(create_company)
    
    async def test_check_create_user_without_permissons(self, client:AsyncClient, create_user:Users, db:AsyncSession):
        response = await client.post(app.url_path_for('create_job'), 
            json=self.json
        )
        assert response.status_code == 403
        await db.delete(create_user)

class TestupdateJobs:
    update_json  = {
    "title": "New title",
    "description": "new string",
    "salary_from": 1000,
    "salary_to": 5000,
    "is_active": True
    }
    async def test_update_job_with_permissions(self, create_job:Jobs, client:AsyncClient, db:AsyncSession):

        token = create_access_token({"sub": str(create_job.user_id)})
        headers = {
            'accept': 'application/json',
            'Authorization' : f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = await client.put(app.url_path_for('update_job'), 
            json=self.update_json,
            headers = headers,
            params={'id':create_job.id}
        )
        assert response.status_code == 200
        
        await db.delete(create_job)
        company = await Users_CRUD.get_by_id(create_job.user_id, db)
        await db.delete(company)

    async def test_update_job_without_permissions(self, create_user:Users, client:AsyncClient, db:AsyncSession):
        response = await client.put(app.url_path_for('update_job'), 
            json=self.update_json,
            params={'id':create_user.id}
        )
        assert response.status_code == 403
        
        await db.delete(create_user)

class TestDeleteJob:
    async def test_delete_with_permissions(self, client:AsyncClient, create_job:Jobs, db:AsyncSession):
        token = create_access_token({"sub": str(create_job.user_id)})
        headers = {
            'accept': 'application/json',
            'Authorization' : f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        response = await client.delete(app.url_path_for('delete_job'), 
            headers = headers,
            params={'id':create_job.id}
        )
        assert response.status_code == 200

        await db.delete(create_job)
        company = await Users_CRUD.get_by_id(create_job.user_id, db)
        await db.delete(company)
    
    async def test_delete_without_permissions(self, client:AsyncClient, create_job:Jobs, db:AsyncSession):
        response = await client.delete(app.url_path_for('delete_job'), 
            params={'id':create_job.id}
        )
        assert response.status_code == 403

        await db.delete(create_job)
        company = await Users_CRUD.get_by_id(create_job.user_id, db)
        await db.delete(company)



