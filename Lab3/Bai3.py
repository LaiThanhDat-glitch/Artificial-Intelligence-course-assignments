def solve_system_backtracking():
    domain = list(range(-10, 11))  # [-10, 10]
    solutions = []
    
    # Backtrack gán x trước, sau đó gán y và tỉa nhánh dựa trên ràng buộc
    for x in domain:
        # Tỉa nhánh sớm với C1: 2y = 25 - 3x.
        # Vì y in [-10, 10] nên 25 - 3x phải là số chẵn và nằm trong [-20, 20]
        rem = 25 - 3 * x
        if rem < -20 or rem > 20 or rem % 2 != 0:
            continue
            
        for y in domain:
            # Kiểm tra ràng buộc thứ nhất
            constraint1 = (3 * x + 2 * y == 25)
            if not constraint1:
                continue
                
            # Kiểm tra ràng buộc thứ hai
            constraint2 = (2 * x - y == 5)
            if not constraint2:
                continue
                
            solutions.append((x, y))
            
    return solutions

if __name__ == "__main__":
    print("\n=== BÀI 3: HỆ PHƯƠNG TRÌNH NGHIỆM NGUYÊN BẰNG BACKTRACKING ===")
    sols = solve_system_backtracking()
    if sols:
        for x, y in sols:
            print(f"Tìm thấy nghiệm nguyên: x = {x}, y = {y}")
            print(f"  Kiểm tra C1: 3*({x}) + 2*({y}) = {3*x + 2*y} (Thỏa mãn = 25)")
            print(f"  Kiểm tra C2: 2*({x}) - ({y}) = {2*x - y} (Thỏa mãn = 5)")
    else:
        print("Không có nghiệm nguyên trong khoảng [-10, 10].")