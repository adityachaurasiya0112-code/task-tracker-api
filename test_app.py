def test_health(client):
    res = client.get("/health")
    assert res.status_code == 999  # jaan-bujh kar galat kiya
    assert res.get_json()["status"] == "ok"import pytest
from app import app, tasks

@pytest.fixture
def client():
    tasks.clear()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_create_task(client):
    res = client.post("/tasks", json={"title": "Learn Jenkins"})
    assert res.status_code == 201
    assert res.get_json()["title"] == "Learn Jenkins"

def test_create_task_missing_title(client):
    res = client.post("/tasks", json={})
    assert res.status_code == 400

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    res = client.get("/tasks")
    assert res.status_code == 200
    assert len(res.get_json()) == 1

def test_update_task(client):
    create_res = client.post("/tasks", json={"title": "Task 1"})
    task_id = create_res.get_json()["id"]
    res = client.put(f"/tasks/{task_id}", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True

def test_delete_task(client):
    create_res = client.post("/tasks", json={"title": "Task 1"})
    task_id = create_res.get_json()["id"]
    res = client.delete(f"/tasks/{task_id}")
    assert res.status_code == 200
