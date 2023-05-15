from typing import Dict

from enowshop.endpoints.helpers import float_to_int
from enowshop.endpoints.paginate import paginate
from enowshop.endpoints.products.repository import ProductsRepository, CategoryProductsRepository, CategoryRepository
from enowshop.endpoints.promotions.repository import PromotionsRepository


class ProductsService:
    def __init__(self, products_repository: ProductsRepository, category_repository: CategoryRepository,
                 category_products_repository: CategoryProductsRepository,
                 promotion_products: PromotionsRepository):
        self.products_repo = products_repository
        self.category_repo = category_repository
        self.category_products = category_products_repository
        self.promotion_products = promotion_products

    async def register_product(self, product: dict):
        category = await self.category_repo.filter_by({'uuid': product.pop('category_uuid')})
        product['price'] = float_to_int(product['price'])
        product = await self.products_repo.create(product)
        await self.category_products.create({'category_id': category.id, 'product_id': product.id})

        return product

    async def get_all_products(self):
        return await self.products_repo.get_all()

    async def get_product_by_uuid(self, product_uuid: str):
        return await self.products_repo.get_product_with_category({'uuid': product_uuid})

    async def get_all_products_with_category(self, params: Dict):
        products_id = []
        if params.get('category'):
            category = await self.category_repo.filter_by({'uuid': params.pop('category')})
            products_id = await self.category_products.get_all_products_id_by_category(category_id=category.id)

        results, total = await self.products_repo.get_all_products_with_category(params=params, products_id=products_id)
        return paginate(results, params.get('offset'), total)

    async def update_product_by_uuid(self, product_id, product):
        product['price'] *= 100
        await self.products_repo.update_by_uuid(pk=product_id, values=product)

    async def change_status_active(self, product_uuid, action):
        actions = {
            'activate': self.products_repo.reactivate_by_uuid,
            'deactivate': self.products_repo.soft_delete_by_uuid
        }
        await actions[action](product_uuid)

    @staticmethod
    def calc_new_price(results):
        for result in results:
            setattr(result, 'new_price', result.price - (result.price * (result.promotion.discount / 100)))
        return results

    async def get_products_by_promotion(self, promotion_uuid, params: Dict):
        results, total = await self.products_repo.get_product_by_promotion_uuid(promotion_uuid=promotion_uuid,
                                                                                params=params)
        results = self.calc_new_price(results)
        return paginate(results, params.get('offset'), total)