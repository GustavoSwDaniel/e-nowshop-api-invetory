import uvicorn
from enowshop.middlewares.exception_handler import generic_request_exception_handler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import HTTPStatusError


def create_app() -> False:
    app = FastAPI()
    from enowshop.infrastructure.containers import Container
    container = Container()

    from enowshop.endpoints.category import controller as category_module
    category_module.configure(app)

    from enowshop.endpoints.products import controller as product_module
    product_module.configure(app)

    from enowshop.endpoints.promotions import controller as promotion_module
    promotion_module.configure(app)

    from enowshop.domain.s3 import controller as s3_module
    s3_module.configure(app)

    container.wire(modules=[category_module, product_module, promotion_module, s3_module])

    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'],
                       allow_headers=['*'])

    app.add_exception_handler(HTTPStatusError, handler=generic_request_exception_handler)

    return app


api_app = create_app()

if __name__ == '__main__':
    uvicorn.run(api_app, host='0.0.0.0', port=8081)
