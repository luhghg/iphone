from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.routers import (auth_router, category_router,
                         product_router, product_variant_router,
                         product_image_router, cart_router, order_router)
from app.db.session import async_engine as engine
from app.core.admin import setup_admin 


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(category_router.router)
app.include_router(product_router.router)
app.include_router(product_variant_router.router)
app.include_router(product_image_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)
setup_admin(app, engine)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
