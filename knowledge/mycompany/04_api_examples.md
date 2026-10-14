可以，这里给你一份**可直接一键复制**的完整内容，你直接全选、复制、覆盖到 `knowledge/mycompany/04_api_examples.md` 即可：

```markdown
# 商品管理系统 API 接口文档

> 基础路径：http://127.0.0.1:8200
> 所有请求和响应均为 JSON 格式（Content-Type: application/json）。
> 业务错误码通过 HTTP 状态码 + 响应体中的业务码字段双重表达。

---

## 1. 创建商品

- 方法：POST
- 路径：/api/products
- 功能：管理员创建一个新商品，系统自动分配唯一 ID。
- 请求体字段：
  - name：string，必填，长度 1~50 字符，全局唯一
  - price：float，必填，范围 0.01 ~ 99999.99
  - stock：int，必填，范围 0 ~ 9999

- 请求示例：
```json
{
  "name": "机械键盘",
  "price": 299.00,
  "stock": 100
}
```

- 成功响应：HTTP 201
```json
{
  "id": 1,
  "name": "机械键盘",
  "price": 299.00,
  "stock": 100
}
```

- 失败响应：
  - 400 INVALID_NAME：name 为空或超过 50 字符
  - 400 INVALID_PRICE：price 不在 0.01 ~ 99999.99 之间
  - 400 INVALID_STOCK：stock 不在 0 ~ 9999 之间
  - 409 DUPLICATE_NAME：商品名已存在

---

## 2. 查询商品详情

- 方法：GET
- 路径：/api/products/{id}
- 功能：根据商品 ID 查询商品详情。
- 路径参数：
  - id：int，必填，商品唯一标识

- 请求示例：
```
GET /api/products/1
```

- 成功响应：HTTP 200
```json
{
  "id": 1,
  "name": "机械键盘",
  "price": 299.00,
  "stock": 100
}
```

- 失败响应：
  - 404 PRODUCT_NOT_FOUND：指定 ID 的商品不存在

---

## 3. 扣减库存

- 方法：POST
- 路径：/api/products/{id}/deduct
- 功能：下单后扣减指定商品的库存。
- 路径参数：
  - id：int，必填，商品唯一标识

- 请求体字段：
  - quantity：int，必填，正整数，且不能大于当前库存

- 请求示例：
```json
{
  "quantity": 10
}
```

- 成功响应：HTTP 200
```json
{
  "id": 1,
  "stock": 90
}
```

- 失败响应：
  - 400 INVALID_QUANTITY：quantity <= 0
  - 409 INSUFFICIENT_STOCK：quantity 大于当前库存（扣减失败，库存不变）
  - 404 PRODUCT_NOT_FOUND：指定 ID 的商品不存在

---

## 4. 删除商品

- 方法：DELETE
- 路径：/api/products/{id}
- 功能：管理员下架并删除指定商品。
- 路径参数：
  - id：int，必填，商品唯一标识

- 成功响应：HTTP 204（无响应体）

- 失败响应：
  - 404 PRODUCT_NOT_FOUND：指定 ID 的商品不存在

---

## 5. 业务规则索引（供测试用例引用）

| 规则编号 | 规则描述 | 关联接口 |
| :--- | :--- | :--- |
| BR-01 | 商品名唯一 | POST /api/products |
| BR-02 | 价格范围 0.01 ~ 99999.99 | POST /api/products |
| BR-03 | 库存范围 0 ~ 9999 | POST /api/products |
| BR-04 | 扣减库存不能超卖 | POST /api/products/{id}/deduct |
| BR-05 | 扣减数量必须为正整数 | POST /api/products/{id}/deduct |
| BR-06 | 删除后不可查询 | DELETE /api/products/{id}、GET /api/products/{id} |
| BR-07 | 并发扣减最后一件库存时，只能有一个成功 | POST /api/products/{id}/deduct |
```

放好后记得：
1. 确认 `knowledge/manifest.json` 里 `mycompany` 的 `documents` 包含 `00_BRD.md`、`01_business_rules.md`、`04_api_examples.md`。
2. 重建知识库：
```powershell
python scripts/build_kb.py --reset
```
3. 跑测试验证：
```powershell
cd mycompany_api_test
pytest test_product.py -v
```