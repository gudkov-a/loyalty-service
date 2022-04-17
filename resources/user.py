from flasgger import SwaggerView

from app.models import Customer
from app.schemas import UserResponseSchema


class CustomersList(SwaggerView):

    definitions = {'UserResponseSchema': UserResponseSchema}

    def get(self):
        """
        List of customers
        ---
        tags:
          - customer
        responses:
          200:
            schema:
              $ref: '#/definitions/UserResponseSchema'
        """
        customers = Customer.query.all()
        return UserResponseSchema(many=True).dump(customers)
