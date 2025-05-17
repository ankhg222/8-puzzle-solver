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


        2.1.5. Nhận xét về hiệu suất của các thuật toán Tìm kiếm không có thông tin

            Khi áp dụng vào trò chơi 8 ô chữ (8-Puzzle), mỗi thuật toán trong nhóm Uninformed Search có những ưu nhược điểm riêng:

                BFS là thuật toán ổn định và đáng tin cậy nhất trong nhóm này. Nó luôn tìm ra đường đi ngắn nhất nếu tồn tại, nhưng phải đánh đổi bằng việc mở rộng rất nhiều trạng thái trong bộ nhớ.

                DFS có lợi thế về tốc độ và sử dụng ít bộ nhớ hơn, tuy nhiên dễ rơi vào nhánh sai, không đảm bảo tìm được lời giải tối ưu, đặc biệt với trạng thái ban đầu phức tạp.

                UCS đảm bảo tìm lời giải tối ưu tương tự như BFS trong trường hợp mọi bước đi có cùng chi phí, nhưng vận hành nặng hơn do phải xử lý hàng đợi ưu tiên.

                IDDFS kết hợp ưu điểm của DFS và BFS, vừa tiết kiệm bộ nhớ vừa đảm bảo tìm được lời giải tối ưu. Tuy nhiên, nó phải lặp lại quá trình tìm kiếm nhiều lần ở các độ sâu khác nhau, dẫn đến thời gian thực thi lớn hơn đáng kể.

            Trong nhóm các thuật toán không có thông tin, BFS là lựa chọn tốt nhất khi cần một giải pháp đơn giản, đảm bảo tìm lời giải ngắn nhất và dễ kiểm soát. Với bài toán 8 ô chữ có không gian trạng thái vừa phải – BFS hoạt động hiệu quả và là tiêu chuẩn so sánh cho các phương pháp khác.



    2.2. Các thuật toán Tìm kiếm có thông tin

        2.2.1 Greedy Best-First Search
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: Greedy chọn node có giá trị heuristic nhỏ nhất (Manhattan distance) mà không xét chi phí đã đi.
            Tốc độ nhanh, ít mở rộng node nhưng có thể bỏ qua lời giải tối ưu.
            Solution là chuỗi bước đi được chọn theo hướng gần goal nhất.

![](gifs/Greedy.gif)


        2.2.2 A* Search
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: A* sử dụng tổng chi phí đã đi (g(n)) và heuristic ước lượng (h(n)), tức f(n) = g(n) + h(n).
            Thuật toán này luôn tìm được đường đi ngắn nhất nếu h(n) là admissible (Manhattan).
            Solution được tối ưu cả về độ dài và số node mở rộng.

![](gifs/A_Search.gif)


        2.2.3 IDA* (Iterative Deepening A*)
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3.
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Mỗi bước có chi phí bằng 1.

            Solution: IDA* kết hợp ưu điểm của A* và IDDFS: sử dụng f(n) = g(n) + h(n) và cắt tỉa theo ngưỡng.
            Giảm bộ nhớ so với A*, đảm bảo tìm lời giải tối ưu, nhưng thời gian thực thi lâu hơn do phải lặp lại nhiều lần.
            Solution được lưu như danh sách bước hợp lệ đến goal.

![](gifs/IDA.gif)


        2.2.4 Nhận xét về hiệu suất của các thuật toán Tìm kiếm không có thông tin

            Greedy Best-First Search

                Ưu điểm lớn nhất là tốc độ nhanh và số node mở rộng ít.
                Tuy nhiên, do chỉ quan tâm đến khoảng cách ước lượng đến đích (h(n)) mà không xét chi phí đã đi (g(n)), nên Greedy dễ bị đi vòng, dẫn đến lời giải không tối ưu hoặc bị kẹt trong cấu trúc mê cung của trạng thái.
                Greedy hoạt động tốt nếu trạng thái đơn giản, nhưng thiếu ổn định ở các trạng thái khó.

            A Search*

                Là thuật toán nổi bật nhất trong nhóm vì kết hợp được cả chi phí thực tế (g(n)) và heuristic (h(n)) thông qua công thức f(n) = g(n) + h(n).
                Trong bài toán 8-Puzzle, khi sử dụng heuristic Manhattan, A* luôn tìm được lời giải ngắn nhất nếu tồn tại và heuristic là admissible.
                A* có thể mở rộng nhiều node hơn Greedy nhưng đổi lại độ chính xác và tối ưu là vượt trội.

            IDA (Iterative Deepening A)**

                IDA* giữ nguyên tính tối ưu của A* nhưng sử dụng chiến lược sâu dần (Iterative Deepening) để tiết kiệm bộ nhớ.
                Tuy nhiên, nó phải lặp lại quá trình tìm kiếm nhiều lần, dẫn đến thời gian thực thi lâu hơn A*.
                IDA* phù hợp khi bộ nhớ bị hạn chế hoặc khi cần đảm bảo độ tối ưu trong điều kiện bộ nhớ thấp.    

            Trong nhóm Tìm kiếm có thông tin:

                A* là lựa chọn tốt nhất nếu muốn tìm lời giải ngắn nhất, đảm bảo tối ưu, và chấp nhận mở rộng nhiều node hơn.
                Greedy nhanh, phù hợp để chạy thời gian thực hoặc trong các trạng thái đơn giản, nhưng không đảm bảo tối ưu.
                IDA* là phương án thay thế tốt cho A* khi muốn tiết kiệm bộ nhớ, dù đánh đổi bằng thời gian.



    2.3. Các thuật toán Tìm kiếm cục bộ (Local Search)


        2.3.1 Simple Hill Climbing
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Không xét tổng chi phí, chỉ xét heuristic.

            Solution: Ở mỗi bước, thuật toán chọn trạng thái hàng xóm có giá trị heuristic thấp hơn.
            Nếu không có hàng xóm nào tốt hơn → dừng lại. Dễ bị rơi vào cực trị cục bộ.
            Solution là chuỗi các bước cải thiện liên tục đến khi không thể tốt hơn.


![](gifs/Simple_Hill.gif)


        2.3.2 Steepest Ascent Hill Climbing
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Không xét tổng chi phí, chỉ xét heuristic.

            Solution: Ở mỗi bước, thuật toán duyệt tất cả trạng thái hàng xóm và chọn trạng thái có giá trị heuristic nhỏ nhất.
            Việc chọn tốt nhất giúp giảm khả năng kẹt ở cực trị gần, nhưng vẫn có thể mắc kẹt ở cực trị toàn cục.
            Solution là chuỗi các bước tối ưu cục bộ cho đến khi không còn hàng xóm nào tốt hơn.


![](gifs/Steepest_Hill.gif)


        2.3.3 Random Restart Hill Climbing
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Không xét tổng chi phí, chỉ xét heuristic.

            Solution: Thuật toán thực hiện nhiều lần Hill Climbing từ các trạng thái khởi tạo ngẫu nhiên.
            Nếu bị mắc kẹt cục bộ, nó khởi động lại từ trạng thái mới → tăng khả năng tìm được lời giải tốt hơn.
            Solution là lời giải ngắn nhất trong số các lần chạy, nếu tồn tại.

![](gifs/Rand_Hill.gif)


        2.3.4 Simulated Annealing
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Không xét tổng chi phí, chỉ xét heuristic và xác suất lựa chọn.

            Solution: Ở mỗi bước, thuật toán có thể chọn cả trạng thái tệ hơn với một xác suất phụ thuộc vào nhiệt độ hiện tại.
            Nhiệt độ giảm dần theo thời gian, giúp kiểm soát độ "mạo hiểm" và tránh rơi vào cực trị.
            Solution là chuỗi bước tìm kiếm với khả năng thoát khỏi điểm kẹt cục bộ.


![](gifs/Simulated.gif)


        2.3.5 Beam Search
            Trạng thái: Mảng 1 chiều gồm 9 ô, đại diện cho bảng 3x3 (0 là ô trống).
            Trạng thái ban đầu: [2, 6, 5, 0, 8, 7, 4, 3, 1]
            Trạng thái đích: [1, 2, 3, 4, 5, 6, 7, 8, 0]
            Phép toán: Di chuyển 0 lên, xuống, trái, phải nếu hợp lệ.
            Chi phí: Không xét tổng chi phí, chỉ xét heuristic.

            Solution: Tại mỗi bước, thuật toán chỉ giữ lại k trạng thái có heuristic tốt nhất để tiếp tục mở rộng.
            Việc giới hạn số lượng trạng thái giúp giảm chi phí tính toán, nhưng dễ bỏ qua lời giải nếu loại sai.
            Solution là chuỗi bước đi từ trạng thái tốt nhất còn lại trong mỗi vòng mở rộng.

![](gifs/Beam.gif)


        2.3.6 Nhận xét về hiệu suất của các thuật toán Local Search
        
            Simple Hill Climbing

                Thuật toán đơn giản, mỗi bước chỉ chọn trạng thái hàng xóm tốt hơn.
                Tuy nhiên, rất dễ bị kẹt ở cực trị cục bộ nếu xung quanh không có trạng thái nào tốt hơn.
                Trong 8-Puzzle, có thể đứng im giữa chừng nếu chọn nhánh không hợp lý.


            Steepest Ascent Hill Climbing

                Cải tiến hơn Simple Hill Climbing ở chỗ xét tất cả hàng xóm và chọn trạng thái tốt nhất trong số đó.
                Dễ tránh được một số điểm kẹt nhỏ, nhưng vẫn khó thoát khỏi cực trị toàn cục.
                Trong các trạng thái khó, vẫn có thể dừng lại mà không đạt đích.

            Random Restart Hill Climbing

                Giảm rủi ro kẹt cực trị bằng cách chạy nhiều lần Hill Climbing từ các trạng thái khởi đầu khác nhau.
                Nếu một lần bị kẹt → khởi động lại → tăng xác suất tìm được lời giải tốt hơn.
                Kết quả phụ thuộc vào số lần restart và chất lượng khởi tạo ban đầu.
                Trong 8-Puzzle, hiệu quả hơn nhiều so với Simple/Steepest nếu cho phép chạy lặp lại.

            Simulated Annealing

                Có khả năng vượt qua cực trị bằng cách chấp nhận trạng thái tệ hơn với một xác suất nhất định.
                Xác suất này giảm dần theo thời gian (giống như quá trình tôi luyện kim loại – annealing).
                Trong bài toán 8 ô chữ, đây là thuật toán ổn định và hiệu quả nhất trong nhóm Local Search, nếu điều chỉnh thông số nhiệt độ hợp lý.

            Beam Search

                Tối ưu bộ nhớ bằng cách chỉ giữ lại k trạng thái tốt nhất ở mỗi bước (beam width).
                Nếu k quá nhỏ, thuật toán có thể bỏ sót lời giải.
                Nếu k đủ lớn, có thể tìm được kết quả tốt nhanh hơn A*, nhưng không đảm bảo tối ưu.

                
            Simulated Annealing là thuật toán tốt nhất trong nhóm Local Search vì có khả năng thoát khỏi điểm kẹt và khám phá không gian trạng thái tốt hơn.
            Random Restart cũng hiệu quả nếu có đủ số lần thử lại và trạng thái khởi tạo phân tán.
            Simple và Steepest thích hợp cho bài toán đơn giản, nhưng kém hiệu quả ở các trạng thái phức tạp.
            Beam Search hiệu quả với cấu hình phù hợp, nhưng yêu cầu phải chọn k hợp lý để cân bằng giữa tốc độ và độ chính xác.