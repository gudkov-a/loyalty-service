import pytest

from flask.testing import Client


from app import db
from app.models import Brand, DiscountCode


class TestCreateCodes:

    @pytest.fixture
    def create_brand(self):
        brand = Brand(name='xyz')
        db.session.add(brand)
        db.session.flush()
        db.session.commit()

    def test_create_codes_via_endpoint(self, client: Client, create_brand):
        brand_id = Brand.query.first().id
        url = f'/api/brand/{brand_id}/generate_codes'

        desired_amount = 10
        assert DiscountCode.query.filter(DiscountCode.brand_id == brand_id).count() == 0
        response = client.post(url, json={'amount': desired_amount})
        assert response.status_code == 200
        assert DiscountCode.query.filter(DiscountCode.brand_id == brand_id).count() == desired_amount

    def test_create_codes_for_not_existing_brand(self, client: Client):
        assert Brand.query.count() == 0

        url = f'/api/brand/{123}/generate_codes'
        response = client.post(url, json={'amount': 1})
        assert response.status_code == 404
