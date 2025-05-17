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

    2.1.1. Tập hợp trạng thái (State Space)
        Là tất cả các hoán vị hợp lệ của 9 ô số từ 0 đến 8, trong đó số 0 đại diện cho ô trống. Tổng cộng có 9! = 362,880 trạng thái, nhưng chỉ một nửa trong số đó là hợp lệ do tính chất đảo ngược.

    2.1.2 Trạng thái ban đầu (Initial State)
        Là cấu hình khởi đầu của bảng 8 ô, được người dùng hoặc chương trình cung cấp.

    2.1.3. Trạng thái đích (Goal State)
        Là cấu hình mong muốn đạt được, thông thường là:
        [1, 2, 3,
        4, 5, 6,
        7, 8, 0]

    2.1.4 Tập hành động (Actions / Operators)
        Bao gồm các phép di chuyển hợp lệ của ô trống 0 sang vị trí: lên, xuống, trái, phải tương ứng với việc hoán đổi 0 với một số bên cạnh nó theo hướng tương ứng.

    2.1.5 Hàm kế tiếp (Transition Model)
        Mô tả kết quả của việc áp dụng một hành động vào một trạng thái, tạo ra trạng thái mới.
 
    2.1.6 Hàm kiểm tra mục tiêu (Goal Test)
        Kiểm tra xem trạng thái hiện tại có trùng với trạng thái đích hay không. 

    2.1.7 Hàm chi phí 
        Mỗi hành động thường được gán chi phí bằng 1, dẫn đến tổng chi phí bằng số bước đi. 
    
    2.1.8  Solution trong trò chơi 8-Puzzle 
        Trong trò chơi 8-Puzzle, solution (lời giải) là một dãy các bước di chuyển hợp lệ đưa trạng thái ban đầu của bảng về trạng thái đích thông qua việc di chuyển ô trống (0).

    -Cấu trúc của solution
    Mỗi bước trong lời giải tương ứng với một hành động di chuyển 0 theo một trong các hướng: lên, xuống, trái, hoặc phải. Trong chương trình, solution được lưu trữ dưới dạng một danh sách các cặp chỉ số, thể hiện việc hoán đổi giữa 0 và ô số lân cận.

    -Vai trò của solution
    Solution đóng vai trò trung tâm trong quá trình giải bài toán và mô phỏng:

    Là kết quả đầu ra của thuật toán tìm kiếm, thể hiện đường đi từ trạng thái đầu đến trạng thái đích.

    Giúp mô phỏng trực quan quá trình giải qua hoạt ảnh từng bước trong giao diện đồ họa.

    Dùng để đánh giá hiệu quả thuật toán, thông qua:

    Số bước trong solution (độ dài lời giải)

    Thời gian tìm ra solution

    Số node mở rộng để tìm được solution

