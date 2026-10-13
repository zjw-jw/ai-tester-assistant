"""
简易商品管理系统（被测系统）
运行：python mycompany_sut.py
访问：http://127.0.0.1:8200/docs
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="商品管理系统")
products = {}
next_id = 1

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class DeductRequest(BaseModel):
    quantity: int

@app.post("/api/products", status_code=201)
def create_product(p: ProductCreate):
    global next_id
    if not (1 <= len(p.name) <= 50):
        raise HTTPException(400, "INVALID_NAME")
    if not (0.01 <= p.price <= 99999.99):
        raise HTTPException(400, "INVALID_PRICE")
    if not (0 <= p.stock <= 9999):
        raise HTTPException(400, "INVALID_STOCK")
    for prod in products.values():
        if prod["name"] == p.name:
            raise HTTPException(409, "DUPLICATE_NAME")
    prod = {"id": next_id, "name": p.name, "price": p.price, "stock": p.stock}
    products[next_id] = prod
    next_id += 1
    return prod

@app.get("/api/products/{pid}")
def get_product(pid: int):
    if pid not in products:
        raise HTTPException(404, "PRODUCT_NOT_FOUND")
    return products[pid]

@app.post("/api/products/{pid}/deduct")
def deduct_stock(pid: int, req: DeductRequest):
    if pid not in products:
        raise HTTPException(404, "PRODUCT_NOT_FOUND")
    if req.quantity <= 0:
        raise HTTPException(400, "INVALID_QUANTITY")
    if req.quantity > products[pid]["stock"]:
        raise HTTPException(409, "INSUFFICIENT_STOCK")
    products[pid]["stock"] -= req.quantity
    return {"id": pid, "stock": products[pid]["stock"]}

@app.delete("/api/products/{pid}", status_code=204)
def delete_product(pid: int):
    if pid not in products:
        raise HTTPException(404, "PRODUCT_NOT_FOUND")
    del products[pid]
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8200)