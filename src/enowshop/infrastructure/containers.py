from dependency_injector import containers, providers

from config import Config
from enowshop.endpoints.category.repository import CategoryRepository
from enowshop.endpoints.category.service import CategoryService
from enowshop.endpoints.products.repository import ProductsRepository, CategoryProductsRepository
from enowshop.endpoints.products.service import ProductsService
from enowshop.endpoints.promotions.repository import PromotionsRepository
from enowshop.endpoints.promotions.service import PromotionsService
from enowshop.infrastructure.database.database_sql import PostgresDatabase
from enowshop.domain.s3.s3_client import S3Client
from enowshop.domain.s3.service import S3Service


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    postgres_db = providers.Singleton(PostgresDatabase, database_url=Config.DATABASE_URL)

    # repository
    category_repository = providers.Factory(CategoryRepository, session_factory=postgres_db.provided.session)
    category_product_repository = providers.Factory(CategoryProductsRepository,
                                                    session_factory=postgres_db.provided.session)

    products_repository = providers.Factory(ProductsRepository, session_factory=postgres_db.provided.session)
    promotions_repository = providers.Factory(PromotionsRepository, session_factory=postgres_db.provided.session)

    s3_client = providers.Factory(S3Client, s3_bucket_name=Config.S3_BUCKET_NAME,
                                  aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                                  aws_region_name=Config.AWS_REGION_NAME)

    # services
    s3_service = providers.Factory(S3Service, s3_client=s3_client)

    category_service = providers.Factory(CategoryService, category_repository=category_repository)
    product_service = providers.Factory(ProductsService, category_repository=category_repository,
                                        products_repository=products_repository,
                                        category_products_repository=category_product_repository,
                                        promotion_products=promotions_repository)
    promotion_service = providers.Factory(PromotionsService, promotions_repository=promotions_repository)
