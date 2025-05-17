1. Mục tiêu


Mục tiêu của dự án này là xây dựng một ứng dụng tương tác có khả năng giải quyết bài toán 8-Puzzle thông qua việc triển khai và so sánh nhiều thuật toán tìm kiếm trí tuệ nhân tạo trong một môi trường đồ họa trực quan.

Thông qua dự án, người thực hiện hướng đến các mục tiêu cụ thể sau:

    -Áp dụng lý thuyết trí tuệ nhân tạo vào thực tế, đặc biệt là các chiến lược tìm kiếm trạng thái như tìm kiếm không có thông tin, tìm kiếm có thông tin, tìm kiếm cục bộ, tìm kiếm trong môi trường không xác định và thuật toán học tăng cường.

    -Trực quan hóa quá trình giải bài toán thông qua giao diện đồ họa sử dụng thư viện Pygame, giúp người học hiểu rõ cách thuật toán hoạt động qua từng bước chuyển trạng thái.

    -Phân tích và đánh giá hiệu suất của các thuật toán dựa trên các tiêu chí định lượng như: số bước giải, số lượng node mở rộng, và thời gian thực thi.

    -Khám phá khả năng ứng dụng các thuật toán học tăng cường (Reinforcement Learning) và thuật toán tiến hóa (Genetic Algorithm) trong việc giải quyết các bài toán dạng tổ hợp, nhằm tìm hiểu giới hạn và khả năng tổng quát hóa của các phương pháp này.

    -Tăng cường kỹ năng lập trình thuật toán, tối ưu hóa mã nguồn và kiểm thử phần mềm, đồng thời nâng cao khả năng trình bày báo cáo kỹ thuật, đặc biệt là trình bày logic thuật toán dưới dạng mô phỏng.

2. Nội dung


    2.1. Các thuật toán Tìm kiếm không có thông tin


        2.1.1 Breadth-First Search (BFS)

            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).

            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]

            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0].

            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.

            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: Là chuỗi bước ngắn nhất từ trạng thái ban đầu đến đích, được lưu dưới dạng danh sách các cặp (from_idx, to_idx).


![](gifs/BFS.gif)

        2.1.2 Depth-First Search (DFS)

            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).

            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]

            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]

            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.

            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: DFS mở rộng node theo chiều sâu thay vì chiều rộng.
            Tuy không đảm bảo tìm được đường đi ngắn nhất, nhưng có thể nhanh hơn nếu lời giải nằm ở nhánh đầu.

            Nếu không giới hạn độ sâu, thuật toán dễ rơi vào vòng lặp vô hạn.

            Solution được lưu dưới dạng danh sách các bước (from_idx, to_idx) dẫn đến trạng thái đích.

![](gifs/DFS.gif)

        2.1.3 Uniform Cost Search (UCS)

            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).

            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]

            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]

            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.

            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: UCS sử dụng hàng đợi ưu tiên (priority queue) để 
            chọn bước đi có tổng chi phí nhỏ nhất tính đến hiện tại.

            Trong bài toán này, vì mọi bước đều có chi phí bằng nhau, UCS cho kết quả giống BFS nhưng có thêm chi phí xử lý heap.

            Solution là chuỗi bước hợp lệ tối ưu, được lưu dưới dạng các cặp (from_idx, to_idx).

![](gifs/UCS.gif)

        2.1.4 Iterative Deepening Depth-First Search (IDDFS)

            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).

            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1].
            
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.

            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: IDDFS là sự kết hợp giữa DFS và BFS.

            Thuật toán thực hiện DFS nhiều lần với các giới hạn độ sâu tăng dần cho đến khi tìm được lời giải.

            Ưu điểm của IDDFS là tiết kiệm bộ nhớ như DFS, nhưng vẫn có thể tìm được lời giải tối ưu nếu chi phí mỗi bước là như nhau.

            Solution là chuỗi bước đầu tiên tìm được tại độ sâu tối thiểu và được lưu dưới dạng danh sách (from_idx, to_idx).

![](gifs/IDDFS.gif)


    Nhận xét về hiệu suất của các thuật toán Tìm kiếm không có thông tin

    Khi áp dụng vào trò chơi 8 ô chữ (8-Puzzle), mỗi thuật toán trong nhóm Uninformed Search có những ưu nhược điểm riêng:

        BFS là thuật toán ổn định và đáng tin cậy nhất trong nhóm này. Nó luôn tìm ra đường đi ngắn nhất nếu tồn tại, nhưng phải đánh đổi bằng việc mở rộng rất nhiều trạng thái trong bộ nhớ.

        DFS có lợi thế về tốc độ và sử dụng ít bộ nhớ hơn, tuy nhiên dễ rơi vào nhánh sai, không đảm bảo tìm được lời giải tối ưu, đặc biệt với trạng thái ban đầu phức tạp.

        UCS đảm bảo tìm lời giải tối ưu tương tự như BFS trong trường hợp mọi bước đi có cùng chi phí, nhưng vận hành nặng hơn do phải xử lý hàng đợi ưu tiên.

        IDDFS kết hợp ưu điểm của DFS và BFS, vừa tiết kiệm bộ nhớ vừa đảm bảo tìm được lời giải tối ưu. Tuy nhiên, nó phải lặp lại quá trình tìm kiếm nhiều lần ở các độ sâu khác nhau, dẫn đến thời gian thực thi lớn hơn đáng kể.

    Kết luận:
    
    Trong nhóm các thuật toán không có thông tin, BFS là lựa chọn tốt nhất khi cần một giải pháp đơn giản, đảm bảo tìm lời giải ngắn nhất và dễ kiểm soát. Với bài toán 8 ô chữ có không gian trạng thái vừa phải – BFS hoạt động hiệu quả và là tiêu chuẩn so sánh cho các phương pháp khác.

