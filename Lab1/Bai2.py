import math
from typing import Sequence, Union


class Vector:
    DIMENSION: int = 24

    def __init__(self, components: Sequence[Union[int, float]]):
        """Khởi tạo vector 24 chiều."""
        if len(components) != self.DIMENSION:
            raise ValueError(
                f"Vector phải có đúng {self.DIMENSION} chiều, nhận được {len(components)}."
            )
        self.components = [float(x) for x in components]

    def __repr__(self) -> str:
        # Hiển thị các giá trị dạng số nguyên/thực gọn gàng
        vals = ", ".join(f"{int(x) if x.is_integer() else x:.2f}" for x in self.components)
        return f"[{vals}]"

    def __add__(self, other: "Vector") -> "Vector":
        """Phép cộng: v1 + v2"""
        return Vector([a + b for a, b in zip(self.components, other.components)])

    def __sub__(self, other: "Vector") -> "Vector":
        """Phép trừ: v1 - v2"""
        return Vector([a - b for a, b in zip(self.components, other.components)])

    def dot(self, other: "Vector") -> float:
        """Tích vô hướng: v1 . v2"""
        return sum(a * b for a, b in zip(self.components, other.components))

    def magnitude(self) -> float:
        """Tính module (độ dài L2 norm)."""
        return math.sqrt(sum(x**2 for x in self.components))

    def angle_with(self, other: "Vector", in_degrees: bool = True) -> float:
        """Tính góc giữa 2 vector."""
        norm_product = self.magnitude() * other.magnitude()
        if norm_product == 0:
            raise ValueError("Không thể tính góc với vector 0.")
        cos_sim = max(-1.0, min(1.0, self.dot(other) / norm_product))
        rad = math.acos(cos_sim)
        return math.degrees(rad) if in_degrees else rad

    def cosine_distance(self, other: "Vector") -> float:
        """Tính khoảng cách cosin: 1 - cosine_similarity"""
        norm_product = self.magnitude() * other.magnitude()
        if norm_product == 0:
            raise ValueError("Không thể tính khoảng cách cosin với vector 0.")
        cos_sim = max(-1.0, min(1.0, self.dot(other) / norm_product))
        return 1.0 - cos_sim


def text_to_vector_24(text: str) -> Vector:
    """
    Chuyển văn bản thành vector 24 chiều đại diện cho số lần xuất hiện
    của 24 chữ cái từ 'a' đến 'x' (không phân biệt chữ hoa/thường).
    """
    text_lower = text.lower()
    # 24 ký tự: ord('a') -> ord('x') (từ mã ASCII 97 đến 120)
    counts = [text_lower.count(chr(ord('a') + i)) for i in range(24)]
    return Vector(counts)


# ==========================================
# CHẠY THỬ VÀ KIỂM TRA LẦN LƯỢT CÁC PHƯƠNG THỨC
# ==========================================

# 1. Văn bản gốc và văn bản sau khi xóa bớt từ
doc1 = "The quick brown fox jumps over the lazy dog and laughs loudly"
doc2 = "The quick brown fox jumps and laughs"  # Đã xóa: 'over', 'the', 'lazy', 'dog', 'loudly'

v1 = text_to_vector_24(doc1)
v2 = text_to_vector_24(doc2)

print("=== BÀI TOÁN XÂY DỰNG VECTOR TỪ VĂN BẢN ===")
print(f"Văn bản 1 (gốc)        : \"{doc1}\"")
print(f"Văn bản 2 (đã xóa từ) : \"{doc2}\"")
print()
print("Các chiều tương ứng từ 'a' đến 'x':")
print("['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x']")
print(f"Vector 1: {v1}")
print(f"Vector 2: {v2}")
print("-" * 55)

# 2. Kiểm tra các phương thức của lớp Vector
print("=== KẾT QUẢ TEST CÁC PHƯƠNG THỨC ===")
print("1. Phép cộng (v1 + v2)        :", v1 + v2)
print("2. Phép trừ (v1 - v2)         :", v1 - v2)
print(f"3. Tích vô hướng (v1 . v2)    : {v1.dot(v2):.4f}")
print(f"4. Module (Độ dài v1)         : {v1.magnitude():.4f}")
print(f"   Module (Độ dài v2)         : {v2.magnitude():.4f}")
print(f"5. Góc giữa 2 vector (độ)     : {v1.angle_with(v2):.4f}°")
print(f"   Góc giữa 2 vector (rad)    : {v1.angle_with(v2, in_degrees=False):.4f} rad")
print(f"6. Khoảng cách Cosin          : {v1.cosine_distance(v2):.6f}")
print(f"   (Độ tương đồng Cosin       : {1.0 - v1.cosine_distance(v2):.6f})")