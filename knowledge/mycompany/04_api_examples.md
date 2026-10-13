# 商品管理接口文档

## 1. 创建商品
- 方法：POST
- 路径：/api/products
- 请求体：
  - name: 商品名，必填，1-50 字符
  - price: 价格，必填，0.01-99999.99
  - stock: 库存，必填，0-9999 的整数
- 成功：201，返回 `{ "id": 1, "name": "...", "price": ..., "stock": ... }`
- 失败：
  - 400 INVALID_PRICE：价格不合法
  - 409 DUPLICATE_NAME：商品名已存在

## 2. 查询商品
- 方法：GET
- 路径：/api/products/{id}
- 成功：200，返回商品详情
- 失败：404 PRODUCT_NOT_FOUND

## 3. 扣减库存
- 方法：POST
- 路径：/api/products/{id}/deduct
- 请求体：quantity，必填，正整数
- 成功：200，返回剩余库存
- 失败：
  - 400 INVALID_QUANTITY：数量非法
  - 409 INSUFFICIENT_STOCK：库存不足

## 4. 删除商品
- 方法：DELETE
- 路径：/api/products/{id}
- 成功：204
- 失败：404 PRODUCT_NOT_FOUND