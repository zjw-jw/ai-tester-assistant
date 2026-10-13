# 商品管理业务规则

## BR-01 商品名唯一
同一商品名不能重复创建，重复时返回 409 DUPLICATE_NAME。

## BR-02 价格范围
价格必须在 0.01 到 99999.99 之间，超出返回 400 INVALID_PRICE。

## BR-03 库存范围
库存必须是 0 到 9999 的整数，超出返回 400 INVALID_STOCK。

## BR-04 扣减库存不能超卖
扣减数量大于当前库存时，返回 409 INSUFFICIENT_STOCK，库存不变。

## BR-05 扣减数量必须为正
扣减数量 <= 0 时，返回 400 INVALID_QUANTITY。

## BR-06 删除商品后不可查询
删除后再次查询，返回 404 PRODUCT_NOT_FOUND。