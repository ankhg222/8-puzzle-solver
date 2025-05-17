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
        2.1.1 BFS – Breadth-First Search
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).

            Trạng thái ban đầu: Cung cấp đầu vào.

            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0].

            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.

            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: Là chuỗi bước ngắn nhất từ trạng thái ban đầu đến đích, được lưu dưới dạng danh sách các cặp (from_idx, to_idx).

            ![Mô phỏng thuật toán BFS](gifs/BFS.gif)
