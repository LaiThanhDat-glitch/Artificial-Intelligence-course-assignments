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
        preview = ", ".join(f"{x:.1f}" for x in self.components[:3])
        return f"Vector24D([{preview}, ..., {self.components[-1]:.1f}])"

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
        """Tính module (độ dài) của vector."""
        return math.sqrt(sum(x**2 for x in self.components))

    def angle_with(self, other: "Vector", in_degrees: bool = True) -> float:
        """Tính góc giữa 2 vector (mặc định theo độ)."""
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


# --- CHẠY THỬ VÀ IN KẾT QUẢ ĐẦY ĐỦ CÁC YÊU CẦU ---
v1 = Vector([1.0] * 24)
v2 = Vector([float(i) for i in range(1, 25)])

print("=== KẾT QUẢ THỰC HIỆN CÁC YÊU CẦU ===")
print("Vector 1:", v1)
print("Vector 2:", v2)
print("---------------------------------------")
print("1. Phép cộng (v1 + v2)        :", v1 + v2)
print("2. Phép trừ (v1 - v2)         :", v1 - v2)
print(f"3. Tích vô hướng (v1 . v2)    : {v1.dot(v2):.4f}")
print(f"4. Module v1                  : {v1.magnitude():.4f}")
print(f"   Module v2                  : {v2.magnitude():.4f}")
print(f"5. Góc giữa v1 và v2 (độ)     : {v1.angle_with(v2):.4f}°")
print(f"   Góc giữa v1 và v2 (radian) : {v1.angle_with(v2, in_degrees=False):.4f} rad")
print(f"6. Khoảng cách cosin          : {v1.cosine_distance(v2):.6f}")