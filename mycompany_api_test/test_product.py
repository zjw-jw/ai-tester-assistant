
"""
商品管理系统 (mycompany) - 自动化测试用例
基于 AI 生成的 22 条用例表格，转换为 pytest 脚本。
运行前请确保被测系统已启动：python mycompany_sut.py (默认端口 8200)
"""
import pytest
import requests
import threading
import time
import random
import string

BASE_URL = "http://127.0.0.1:8200"


# ================= 辅助函数 =================

def _random_name(prefix="测试商品"):
    """生成随机商品名，避免不同用例之间名字冲突"""
    return f"{prefix}_{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"


def _create_product(name=None, price=19.9, stock=100):
    """辅助建商品，返回商品 ID。若建失败则抛出异常。"""
    if name is None:
        name = _random_name()
    payload = {"name": name, "price": price, "stock": stock}
    resp = requests.post(f"{BASE_URL}/api/products", json=payload)
    # 如果是预期外的失败，直接抛错中断用例
    if resp.status_code != 201:
        raise Exception(f"建商品失败: {resp.status_code} {resp.text}")
    return resp.json()["id"]


def _delete_product(pid):
    """辅助删商品，用于清理数据（某些用例需要干净环境）"""
    requests.delete(f"{BASE_URL}/api/products/{pid}")


# ================= 测试用例 =================

class TestProductCreation:
    """针对 POST /api/products 的用例"""

    def test_tc_prod_001_create_product_success(self):
        """TC-PROD-001: 正常创建商品"""
        name = _random_name("正常商品")
        payload = {"name": name, "price": 19.9, "stock": 100}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)

        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == name
        assert data["price"] == 19.9
        assert data["stock"] == 100
        assert "id" in data

    def test_tc_prod_002_duplicate_name_rejected(self):
        """TC-PROD-002: 重复商品名创建失败"""
        name = _random_name("重复商品")
        # 先建一个
        _create_product(name=name)
        # 再建同名
        resp = requests.post(f"{BASE_URL}/api/products", json={"name": name, "price": 29.9, "stock": 50})

        assert resp.status_code == 409
        assert "DUPLICATE_NAME" in resp.text

    def test_tc_prod_003_empty_name_rejected(self):
        """TC-PROD-003: 商品名为空创建失败"""
        payload = {"name": "", "price": 19.9, "stock": 100}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 400
        assert "INVALID_NAME" in resp.text

    def test_tc_prod_004_name_too_long_rejected(self):
        """TC-PROD-004: 商品名超过50字符"""
        payload = {"name": "A" * 51, "price": 19.9, "stock": 100}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 400
        assert "INVALID_NAME" in resp.text

    def test_tc_prod_005_price_lower_boundary(self):
        """TC-PROD-005: 价格边界值-下界 (0.01)"""
        payload = {"name": _random_name("底价商品"), "price": 0.01, "stock": 10}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 201

    def test_tc_prod_006_price_below_lower_boundary(self):
        """TC-PROD-006: 价格边界值-下界-1 (0.00)"""
        payload = {"name": _random_name("负价商品"), "price": 0.00, "stock": 10}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 400
        assert "INVALID_PRICE" in resp.text

    def test_tc_prod_007_price_upper_boundary(self):
        """TC-PROD-007: 价格边界值-上界 (99999.99)"""
        payload = {"name": _random_name("天价商品"), "price": 99999.99, "stock": 10}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 201

    def test_tc_prod_008_price_above_upper_boundary(self):
        """TC-PROD-008: 价格边界值-上界+1 (100000.00)"""
        payload = {"name": _random_name("超价商品"), "price": 100000.00, "stock": 10}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 400
        assert "INVALID_PRICE" in resp.text

    def test_tc_prod_009_stock_lower_boundary(self):
        """TC-PROD-009: 库存边界值-下界 (0)"""
        payload = {"name": _random_name("零库存商品"), "price": 19.9, "stock": 0}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 201

    def test_tc_prod_010_stock_above_upper_boundary(self):
        """TC-PROD-010: 库存边界值-上界+1 (10000)"""
        payload = {"name": _random_name("超库存商品"), "price": 19.9, "stock": 10000}
        resp = requests.post(f"{BASE_URL}/api/products", json=payload)
        assert resp.status_code == 400
        assert "INVALID_STOCK" in resp.text


class TestProductQuery:
    """针对 GET /api/products/{id} 的用例"""

    def test_tc_prod_011_get_product_success(self):
        """TC-PROD-011: 正常查询商品"""
        pid = _create_product(name=_random_name("查询商品"))
        resp = requests.get(f"{BASE_URL}/api/products/{pid}")
        assert resp.status_code == 200
        assert resp.json()["id"] == pid

    def test_tc_prod_012_get_nonexistent_product(self):
        """TC-PROD-012: 查询不存在的商品"""
        resp = requests.get(f"{BASE_URL}/api/products/99999")
        assert resp.status_code == 404
        assert "PRODUCT_NOT_FOUND" in resp.text


class TestStockDeduction:
    """针对 POST /api/products/{id}/deduct 的用例"""

    def test_tc_prod_013_deduct_success(self):
        """TC-PROD-013: 正常扣减库存"""
        pid = _create_product(stock=100)
        resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": 10})
        assert resp.status_code == 200
        assert resp.json()["stock"] == 90

    def test_tc_prod_014_deduct_zero(self):
        """TC-PROD-014: 扣减数量为0"""
        pid = _create_product(stock=100)
        resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": 0})
        assert resp.status_code == 400
        assert "INVALID_QUANTITY" in resp.text

    def test_tc_prod_015_deduct_negative(self):
        """TC-PROD-015: 扣减数量为负数"""
        pid = _create_product(stock=100)
        resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": -5})
        assert resp.status_code == 400
        assert "INVALID_QUANTITY" in resp.text

    def test_tc_prod_016_deduct_equal_to_stock(self):
        """TC-PROD-016: 扣减数量等于当前库存"""
        pid = _create_product(stock=10)
        resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": 10})
        assert resp.status_code == 200
        assert resp.json()["stock"] == 0

    def test_tc_prod_017_deduct_exceed_stock(self):
        """TC-PROD-017: 扣减数量超过当前库存"""
        pid = _create_product(stock=10)
        resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": 11})
        assert resp.status_code == 409
        assert "INSUFFICIENT_STOCK" in resp.text

        # 验证失败后数据没有副作用（库存依然为 10）
        check_resp = requests.get(f"{BASE_URL}/api/products/{pid}")
        assert check_resp.json()["stock"] == 10

    @pytest.mark.skip(reason="被测系统未实现幂等机制，无法自动化验证")
    def test_tc_prod_019_deduct_idempotent(self):
        """TC-PROD-019: 扣减接口幂等性"""
        # 原系统 mycompany_sut.py 不接受 request_id 且无幂等逻辑，故跳过
        pass


class TestConcurrency:
    """针对并发场景的用例"""

    def test_tc_prod_018_concurrent_deduct_last_stock(self):
        """TC-PROD-018: 并发扣减最后1个库存"""
        pid = _create_product(stock=1)

        results = []
        def deduct():
            resp = requests.post(f"{BASE_URL}/api/products/{pid}/deduct", json={"quantity": 1})
            results.append(resp.status_code)

        # 启动两个线程同时扣减
        threads = [threading.Thread(target=deduct) for _ in range(2)]
        for t in threads: t.start()
        for t in threads: t.join()

        # 结果应该是一个 200，一个 409
        assert 200 in results
        assert 409 in results

        # 验证最终库存为 0
        check_resp = requests.get(f"{BASE_URL}/api/products/{pid}")
        assert check_resp.json()["stock"] == 0


class TestProductDeletion:
    """针对 DELETE /api/products/{id} 的用例"""

    def test_tc_prod_020_delete_success(self):
        """TC-PROD-020: 正常删除商品"""
        pid = _create_product()
        resp = requests.delete(f"{BASE_URL}/api/products/{pid}")
        assert resp.status_code == 204

    def test_tc_prod_021_delete_nonexistent(self):
        """TC-PROD-021: 删除不存在的商品"""
        resp = requests.delete(f"{BASE_URL}/api/products/99999")
        assert resp.status_code == 404
        assert "PRODUCT_NOT_FOUND" in resp.text

    def test_tc_prod_022_delete_twice(self):
        """TC-PROD-022: 重复删除同一商品"""
        pid = _create_product()
        # 第一次删除
        resp1 = requests.delete(f"{BASE_URL}/api/products/{pid}")
        assert resp1.status_code == 204
        # 第二次删除
        resp2 = requests.delete(f"{BASE_URL}/api/products/{pid}")
        assert resp2.status_code == 404
        assert "PRODUCT_NOT_FOUND" in resp2.text