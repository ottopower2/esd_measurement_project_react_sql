from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_measurement():
    response = client.post(
        "/esd/measurement",
        json={
            "projekt_name": "ESD_Test",
            "test_art": "ESD",
            "voltage_kv": 1,
            "polarity": "positive",
            "test_point": "KL30",
            "operator": "John Doe",
            "hw": "HW123",
        },
    )


    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"


#  test delete measurement
def test_delete_measurement():
    # First, create a measurement to delete
    response = client.post(
        "/esd/measurement",
        json={
            "projekt_name": "ESD_Test_Delete",
            "test_art": "ESD",
            "voltage_kv": 1,
            "polarity": "positive",
            "test_point": "KL30",
            "operator": "John Doe",
            "hw": "HW123",
        },
    )
    assert response.status_code == 200
    measurement_id = response.json()["id"]

    # Now, delete the measurement
    delete_response = client.delete(f"/measurements/{measurement_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "Measurement deleted successfully"}

    # Verify that the measurement is no longer available
    get_response = client.get(f"/measurements/{measurement_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Measurement not found"}



def test_get_measurements_count():
    response = client.get("/measurements/count")
    assert response.status_code == 200
    assert "count" in response.json()
    assert isinstance(response.json()["count"], int)
    # Optionally, you can check that the count is non-negative
    assert response.json()["count"] >= 0


def test_get_operator_by_measurement_id():
    # First, create a measurement to get the operator for
    response = client.post(
        "/esd/measurement",
        json={
            "projekt_name": "ESD_Test_Operator",
            "test_art": "ESD",
            "voltage_kv": 1,
            "polarity": "positive",
            "test_point": "KL30",
            "operator": "John Doe",
            "hw": "HW123",
        },
    )
    assert response.status_code == 200
    measurement_id = response.json()["id"]

    # Now, get the operator by measurement ID
    operator_response = client.get(f"/measurements/{measurement_id}/operator")
    assert operator_response.status_code == 200
    assert operator_response.json() == {"operator": "John Doe"}

    # Clean up by deleting the measurement
    client.delete(f"/measurements/{measurement_id}")
    # Verify that the measurement is no longer available
    get_response = client.get(f"/measurements/{measurement_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Measurement not found"}