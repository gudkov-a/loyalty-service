from flasgger import SwaggerView
from flask_restful import reqparse

from app import db
from app.models import Brand, DiscountCode, Customer
from common.code_utils import CodeGenerator
from common.notify_utils import NotifyHandler


class CreateDiscountCode(SwaggerView):

    def post(self, brand_id: int):
        """
        Create desired amount of discount codes for specific Brand
        ---
        tags:
          - code
        parameters:
          - in: path
            name: brand_id
            type: integer
            required: true
          - in: query
            name: amount
            type: integer
            required: true
        responses:
          200:
            description: Successfully created
          404:
            description: Brand is not found
        """
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=int)
        args = parser.parse_args()

        Brand.query.get_or_404(brand_id)
        amount = args['amount']

        new_codes = CodeGenerator(amount).generate()
        for code in new_codes:
            discount_code = DiscountCode(code=code, brand_id=brand_id)
            db.session.add(discount_code)
        db.session.commit()

        return 200


class GetDiscountCode(SwaggerView):

    def get(self, brand_id: int):
        """
        Get discount code for specific Brand
        ---
        tags:
          - code
        parameters:
          - in: path
            name: brand_id
            type: integer
            required: true
          - in: query
            name: user_id
            type: integer
            required: true
        responses:
          200:
            description: Returns available code
          404:
            description: Brand or User is not found. See response body
          400:
            description: No more codes available
        """
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        args = parser.parse_args()

        brand = Brand.query.get_or_404(brand_id, description='Brand with this id is not found')
        user = Customer.query.get_or_404(args['user_id'], description='Customer with this id is not found')

        code = DiscountCode.query.filter(DiscountCode.brand_id == brand.id,
                                         DiscountCode.issued_to_user.is_(False)
                                         ).first()
        if code is None:
            return 'No more codes available for this Brand', 400

        code_value = code.code
        code.issued_to_user = True
        code.user_id = user.id

        NotifyHandler(brand.name, user.login).notify()

        db.session.commit()
        return code_value
