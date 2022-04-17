from flasgger import SwaggerView

from app.models import Brand
from app.schemas import BrandsResponseSchema


class GetBrands(SwaggerView):

    definitions = {'BrandsResponseSchema': BrandsResponseSchema}

    def get(self):
        """
        Return all the Brand
        ---
        tags:
          - brand
        responses:
          200:
            description: List of Brands
            schema:
              $ref: '#/definitions/BrandsResponseSchema'
        """
        brands = Brand.query.all()
        return BrandsResponseSchema(many=True).dump(brands)
