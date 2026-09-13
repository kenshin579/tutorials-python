"""중첩 모델 - 모델 안에 모델, 재귀 모델, 깊은 중첩 데이터"""

from __future__ import annotations

from pydantic import BaseModel


# --- 중첩 모델 정의 ---
class Address(BaseModel):
    city: str
    zip_code: str


class OrderItem(BaseModel):
    product: str
    quantity: int
    price: float


class Order(BaseModel):
    order_id: str
    items: list[OrderItem]
    shipping_address: Address


# --- 재귀 모델 (트리 구조) ---
class TreeNode(BaseModel):
    name: str
    children: list[TreeNode] = []


class TestNestedModel:
    """중첩 모델"""

    def test_nested_model_creation(self):
        """모델 안에 모델"""
        order = Order(
            order_id="ORD-001",
            items=[
                OrderItem(product="노트북", quantity=1, price=1500000),
                OrderItem(product="마우스", quantity=2, price=35000),
            ],
            shipping_address=Address(city="서울", zip_code="06000"),
        )

        assert order.order_id == "ORD-001"
        assert len(order.items) == 2
        assert order.items[0].product == "노트북"
        assert order.shipping_address.city == "서울"

    def test_nested_model_from_dict(self):
        """dict 데이터에서 중첩 모델 자동 변환"""
        data = {
            "order_id": "ORD-002",
            "items": [
                {"product": "키보드", "quantity": 1, "price": 120000},
            ],
            "shipping_address": {"city": "부산", "zip_code": "48000"},
        }

        order = Order.model_validate(data)

        assert isinstance(order.items[0], OrderItem)
        assert isinstance(order.shipping_address, Address)
        assert order.items[0].product == "키보드"

    def test_nested_model_dump(self):
        """중첩 모델 직렬화"""
        order = Order(
            order_id="ORD-003",
            items=[OrderItem(product="모니터", quantity=1, price=500000)],
            shipping_address=Address(city="대전", zip_code="35000"),
        )

        dumped = order.model_dump()

        assert isinstance(dumped, dict)
        assert isinstance(dumped["items"][0], dict)
        assert dumped["items"][0]["product"] == "모니터"
        assert dumped["shipping_address"]["city"] == "대전"


class TestRecursiveModel:
    """재귀 모델 (트리 구조)"""

    def test_recursive_tree(self):
        """재귀적 트리 구조"""
        tree = TreeNode(
            name="root",
            children=[
                TreeNode(
                    name="child1",
                    children=[
                        TreeNode(name="grandchild1"),
                        TreeNode(name="grandchild2"),
                    ],
                ),
                TreeNode(name="child2"),
            ],
        )

        assert tree.name == "root"
        assert len(tree.children) == 2
        assert tree.children[0].children[0].name == "grandchild1"

    def test_recursive_from_dict(self):
        """dict에서 재귀 모델 변환"""
        data = {
            "name": "폴더A",
            "children": [
                {
                    "name": "폴더B",
                    "children": [{"name": "파일1"}],
                },
            ],
        }

        tree = TreeNode.model_validate(data)

        assert isinstance(tree.children[0], TreeNode)
        assert tree.children[0].children[0].name == "파일1"

    def test_deep_nested_model_validate(self):
        """model_validate로 깊은 중첩 데이터 처리"""
        data = {
            "order_id": "ORD-DEEP",
            "items": [
                {"product": f"상품{i}", "quantity": i, "price": i * 10000}
                for i in range(1, 6)
            ],
            "shipping_address": {"city": "인천", "zip_code": "21000"},
        }

        order = Order.model_validate(data)

        assert len(order.items) == 5
        assert all(isinstance(item, OrderItem) for item in order.items)
        assert order.items[4].product == "상품5"
