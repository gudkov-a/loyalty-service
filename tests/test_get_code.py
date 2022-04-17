import pytest

from flask.testing import Client


from app import db
from app.models import Brand, DiscountCode, Customer
from common.code_utils import CodesGenerator


class TestGetCode:
    brand_name = 'xyz'

    @pytest.fixture
    def create_brand_and_codes(self):
        brand = Brand(name=self.brand_name)
        db.session.add(brand)
        db.session.flush()

        for code in CodesGenerator(10).generate():
            new_code = DiscountCode(code=code, brand_id=brand.id)
            db.session.add(new_code)
        db.session.commit()

    def test_get_code_via_endpoint(self, client: Client, create_brand_and_codes):
        """
        Get the code for particular Brand
        """
        brand = Brand.query.filter_by(name=self.brand_name).first()
        assert brand is not None
        assert DiscountCode.query.filter(DiscountCode.issued_to_user.is_(False),
                                         DiscountCode.used.is_(False)
                                         ).count() > 0
        customer = Customer(login='tester')
        db.session.add(customer)
        db.session.flush()
        customer_id = customer.id
        db.session.commit()

        url = f'/api/brand/{brand.id}/code'
        response = client.get(url, json={'user_id': customer_id})
        assert response.status_code == 200, response.json

        """
        Make sure that code is belong to our user and can be used
        """
        acquired_code = response.json
        code_object = DiscountCode.query.filter_by(code=acquired_code).first()
        assert code_object.user_id == customer_id
        assert code_object.issued_to_user is True
        assert code_object.used is False

        """
        If we ask for another one it will be different code
        """
        response = client.get(url, json={'user_id': customer_id})
        assert response.status_code == 200
        assert response.json != acquired_code

        """
        Now let's take all the codes and check the response status code
        """
        for _ in range(10):
            response = client.get(url, json={'user_id': customer_id})
        assert response.status_code == 400

    def test_get_code_invalid_brand(self, client: Client):
        url = f'/api/brand/{00000}/code'
        response = client.get(url, json={'user_id': 1})
        assert response.status_code == 404
