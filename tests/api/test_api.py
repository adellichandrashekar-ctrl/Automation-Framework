import pytest
import logging

from utils.helpers import Validators, generate_user_payload

logger = logging.getLogger(__name__)

# Test 1 (authentication check)

@pytest.mark.api
@pytest.mark.smoke
class TestUserLogin:
    """POST /auth/login - test authentication seperately"""

    def test_login_success(self, api_client, config):
        """validate login works with valid credentials from config"""
        login_data = {
            "username": config.auth_username,
            "password": config.auth_password
        }
        response = api_client.post("/auth/login", json=login_data)
        Validators.check_status(response, 200)
        Validators.check_key_exists(response, "accessToken")
        logger.info(f"Test Login successfully for: {response.json().get('username')}")
    
    def test_login_failure(self, api_client):
        """Validate login with bad credentials"""
        bad_data = {"username": "wrong", "password": "wrong"}
        response = api_client.post("/auth/login", json=bad_data)
        Validators.check_status(response, 400)

# Test 2 POST create a new user

@pytest.mark.api
@pytest.mark.smoke
class TestCreateUser:
    """POST /users/add - create new users"""

    def test_create_single_user(self, api_client):
        """create a new single user and validate the response"""
        user_data = generate_user_payload(first_name="Chandra", last_name="Shekar")
        response = api_client.post("/users/add", json=user_data)
        Validators.check_status(response, 201)
        data = response.json()
        assert data["firstName"].lower() == "chandra", f"Failed to validate first name, instead we got {data['firstName']}"
        assert data["lastName"].lower() == "shekar", f"Failed to validate last name, instead we got {data['lastName']}"
        logger.info(f"Created New User with ID: {data['id']}")

    @pytest.mark.parametrize("first_name, last_name, role", [("Alice", "Smith", "admin"), ("Bob", "Johnson", "user"), ("Charlie", "Brown", "moderator"),])
    def test_create_multiple_users(self, api_client, first_name, last_name, role):
        """Data driven: create multiple users with different roles"""
        user_data = generate_user_payload(first_name=first_name, last_name=last_name, role=role)
        response = api_client.post("/users/add", json=user_data)
        Validators.check_status(response, 201)
        data = response.json()
        assert data["firstName"] == first_name
        assert data["lastName"] == last_name
        assert data["role"] == role

# Test 3: GET - Read users

@pytest.mark.api
@pytest.mark.smoke
class TestGetUser:
    """Get /users - read users"""

    def test_get_user_by_id(self, api_client):
        response = api_client.get("/user/1")
        Validators.check_status(response, 200)
        Validators.check_key_exists(response, "firstName")
        Validators.check_value(response, "id", 1)

        data = response.json()
        logger.info(f"test_get_user_by_id data: {data}")
        assert "firstName" in data
        assert "email" in data
        assert "role" in data


    def test_get_all_users(self, api_client):
        response = api_client.get("/users")

        Validators.check_status(response, 200)
        data = response.json()
        logger.info(f"test_get_all_users data: {data}")
        assert len(data["users"]) > 0
        logger.info(f"Got {len(data['users'])} users in reponse")

    def test_get_nonexistent_user(self, api_client):
        response = api_client.get("/users/99999")
        Validators.check_status(response, 404)

    @pytest.mark.parametrize("user_id", [1,2,3])
    def test_get_multiple_users_by_id(self, api_client, user_id):
        response = api_client.get(f"/users/{user_id}")
        Validators.check_status(response, 200)
        Validators.check_value(response, "id", user_id)

# Test 4: PUT and PATCH - Update Users

@pytest.mark.api
class TestUpdateUser:
    """PUT and PATCH /users - Update Users"""
    def test_put_update_user_full(self, api_client):
        updated_data = {
            "firstName": "Chandra Updated",
            "lastName": "Shekar Updated",
            "age": 30
        }
        response = api_client.put("/users/1", json=updated_data)
        Validators.check_status(response, 200)
        data = response.json()
        assert data["firstName"].lower() == "chandra updated"
        assert data["lastName"].lower() == "shekar updated"
        logger.info("PUT full update successful")

    def test_patch_update_user_partial(self, api_client):
        """PATCH - update only what is required to updated"""
        partial_data = {"role": "superadmin"}
        response = api_client.patch("/users/1", json=partial_data)

        Validators.check_status(response, 200)
        assert response.json()["role"] == "superadmin"
        logger.info("PATCH partial update successful")

# Test 5: Delete user

@pytest.mark.api
class TestDeleteUser:
    """Delete /users"""

    def test_delete_user(self, api_client):
        """Delete a user and validate it"""
        response = api_client.delete("/users/1")
        Validators.check_status(response, 200)
        data = response.json()
        assert data.get("isDeleted") is True
        assert data.get("id") == 1
        logger.info(f"User 1 is deleted successfully at {data.get('deletedOn')}")

# Full Life Cylce - Single E2E CURD Flow
@pytest.mark.api
@pytest.mark.smoke
class TestUserLifeCycle:
    """Single End to End FLow"""

    def test_full_user_lifecycle(self, api_client):
        """Create user > fetch user > update user > delete user"""
        # CREATE - make a new user (POST call)
        user_data = generate_user_payload(first_name="LifeCycle", last_name="User")
        create_resp = api_client.post("/users/add", json=user_data)
        Validators.check_status(create_resp, 201)
        created_id = create_resp.json()["id"]
        assert create_resp.json()["firstName"] == "LifeCycle"
        logger.info(f"Created user with ID: {created_id}")

        # READ - fetch (GET call)
        get_details = api_client.get("/users/1")
        Validators.check_status(get_details, 200)
        Validators.check_key_exists(get_details, "firstName")
        logger.info(f"FETCHED User: {get_details.json().get('firstName')}")

        # UPDATE - Change the user's name (PUT call)
        update_resp = api_client.put("/users/1", json={"firstName": "Updated"})
        Validators.check_status(update_resp, 200)
        assert update_resp.json()["firstName"].lower() == "updated"
        logger.info("Updated user's name to 'Updated'")

        # Partial update - change only the role (PATCH call)
        patch_resp = api_client.patch("/users/1", json={"role": "Superadmin"})
        Validators.check_status(patch_resp, 200)
        assert patch_resp.json()["role"].lower() == "superadmin"
        logger.info("PATCHED user role to 'Superadmin'")

        # DELETE - remove the user (DELETE call)
        delete_resp = api_client.delete("/users/1")
        Validators.check_status(delete_resp, 200)
        assert delete_resp.json().get("isDeleted") is True
        logger.info("DELETED user -- Full LifeCycle Complete.")

