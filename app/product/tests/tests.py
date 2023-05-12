import pytest
from django.urls import reverse
from .conftest import api_client_with_credentials
from ..models import Product

pytestmark = pytest.mark.django_db


class TestProductCRUD:
    product_list_url = reverse("product:product-list")

    def test_authenticated_user_create_product(
        self, api_client, user_with_specific_permission
    ):
        auth_user = user_with_specific_permission(is_admin=False)
        data = {"name": "Name1", "description": "Just description"}
        api_client_with_credentials(api_client)
        response = api_client.post(self.product_list_url, data)
        assert response.status_code == 201
        returned_json = response.json()
        assert "id" in returned_json
        assert returned_json["name"] == data["name"]
        assert returned_json["description"] == data["description"]
        assert returned_json["user_id"] == auth_user.id

    def test_deny_create_to_nonauthenticated(self, api_client):
        data = {"name": "Name1", "description": "Just description"}
        api_client_with_credentials(api_client)
        response = api_client.post(self.product_list_url, data)
        assert response.status_code == 401

    def test_retrieve_all_products(
        self, api_client, user_with_specific_permission, product_factory
    ):
        user_with_specific_permission(is_admin=False)
        product_factory.create_batch(3)

        api_client_with_credentials(api_client)
        response = api_client.get(self.product_list_url)
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_retrieve_product_detail(
        self, api_client, user_with_specific_permission, product_factory
    ):
        product = product_factory()
        user_with_specific_permission(is_admin=False)

        url = reverse("product:product-detail", kwargs={"pk": str(product.id)})
        api_client_with_credentials(api_client)
        response = api_client.get(url)
        assert response.status_code == 200
        returned_json = response.json()
        assert "id" in returned_json
        assert "name" in returned_json
        assert "description" in returned_json

    def test_admin_delete_product(
        self, api_client, product_factory, user_with_specific_permission
    ):
        product = product_factory()
        user_with_specific_permission(is_admin=True)
        url = reverse("product:product-detail", kwargs={"pk": str(product.id)})
        api_client_with_credentials(api_client)
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Product.objects.count() == 0

    def test_deny_delete_to_nonadmin(
        self, api_client, product_factory, user_with_specific_permission
    ):
        product = product_factory()
        user_with_specific_permission(is_admin=False)
        url = reverse("product:product-detail", kwargs={"pk": str(product.id)})
        api_client_with_credentials(api_client)
        response = api_client.delete(url)
        assert response.status_code == 403
