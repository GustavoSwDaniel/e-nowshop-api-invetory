from enowshop.infrastructure.repositories.repository import SqlRepository
from enowshop_models.models.category import Category


class CategoryRepository(SqlRepository):
    model = Category
