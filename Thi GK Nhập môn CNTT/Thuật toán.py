def Safe_Squares_not_Threaten_with_Bishops(n, bishops):
    safe_squares = 0
    
    diagonal1 = set() 
    diagonal2 = set() 
    
    for bishop in bishops:
        diagonal1.add(bishop[0] + bishop[1])
        diagonal2.add(bishop[0] - bishop[1])
        
    for i in range(n):
        for j in range(n):
            if (i + j) not in diagonal1 and (i - j) not in diagonal2:
                safe_squares += 1
                
    return safe_squares

try:
    n = int(input("Nhập kích thước bàn cờ n: "))
    num_bishops = int(input("Số lượng quân tượng: "))

    bishops_list = []
    for k in range(num_bishops):
        print(f"\nNhập tọa độ quân tượng thứ {k+1}:")
        row = int(input("  - Nhập hàng: "))
        col = int(input("  - Nhập cột: "))
        
        bishops_list.append([row, col])

    result = Safe_Squares_not_Threaten_with_Bishops(n, bishops_list)
    
    print("-" * 30)
    print(f"Kết quả cho n={n}, bishops={bishops_list}")
    print(f"==> SỐ Ô AN TOÀN: {result}") 

except ValueError:
    print("Vui lòng nhập số nguyên hợp lệ!")
