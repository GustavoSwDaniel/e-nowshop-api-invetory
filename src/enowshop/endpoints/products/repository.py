from typing import Dict, List, Tuple, Any

from enowshop_models import CategoryProducts, Category, Promotion
from enowshop_models.models.products import Products
from sqlalchemy import select, update, func
from sqlalchemy.orm import selectinload, load_only

from enowshop.endpoints.paginate import paginate
from enowshop.infrastructure.repositories.repository import SqlRepository


class ProductsRepository(SqlRepository):
    model = Products

    async def get_all_products_with_category(self, params: Dict, products_id: List = None):
        async with self.session_factory() as session:
            query = select(Products).limit(params.get('limit')).offset(params.get('offset'))
            if products_id:
                query = query.where(Products.id.in_(products_id))
            if params.get('min_price'):
                query = query.where(Products.price >= params.get('min_price'))
            if params.get('name'):
                query = query.where(Products.name.like(f'%{params.get("name")}%'))
            if params.get('order_by') == 'created_at':
                query = query.order_by(Products.created_at.desc())

            total = await session.execute(select([func.count(Products.id)]).select_from(Products))
            results = await session.execute(query.options(
                selectinload(Products.category_products).options(selectinload(CategoryProducts.category))))

            total = total.scalar()
            results = results.scalars().all()

            for result in results:
                setattr(result, 'category',
                        [category_products.category for category_products in result.category_products])

        return results, total

    async def get_product_by_promotion_uuid(self, promotion_uuid: str, params) -> Tuple[Any, Any]:
        async with self.session_factory() as session:
            total = await session.execute(select([func.count(self.model.id)])
                                          .join(Promotion, Promotion.id == self.model.promotion_id)
                                          .where(Promotion.uuid == promotion_uuid)
                                          .select_from(Products))

            result = await session.execute(select(self.model).limit(params.get('limit')).offset(params.get('offset'))
                                           .join(Promotion, Promotion.id == self.model.promotion_id)
                                           .where(Promotion.uuid == promotion_uuid)
                                           .options(selectinload(Products.category_products).selectinload(CategoryProducts.category))
                                           .options(selectinload(Products.promotion))
                                           )

            total = total.scalar()
            results = result.scalars().all()

            for result in results:
                setattr(result, 'category',
                        [category_products.category for category_products in result.category_products])

            return results, total

    async def get_product_with_category(self, params: Dict):
        async with self.session_factory() as session:
            result = await session.execute(
                select(Products).filter_by(**params).options(selectinload(Products.category_products)
                                                             .selectinload(CategoryProducts.category)))
            result = result.scalars().first()

            setattr(result, 'category', [category_products.category for category_products in result.category_products])
            return result

    async def update_by_uuid(self, pk, values):
        async with self.session_factory() as session:
            await session.execute(update(self.model).where(self.model.uuid == pk).values(**values))
            await session.commit()


class CategoryProductsRepository(SqlRepository):
    model = CategoryProducts

    async def get_all_products_id_by_category(self, category_id: int) -> List[int]:
        async with self.session_factory() as session:
            result = await session.execute(
                select(self.model.product_id).where(self.model.category_id == category_id)
            )

            return result.scalars().all()


class CategoryRepository(SqlRepository):
    model = Category
