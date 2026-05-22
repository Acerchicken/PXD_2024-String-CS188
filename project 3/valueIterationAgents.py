# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp  # Lưu trữ mô hình MDP được truyền vào hệ thống để truy vấn trạng thái.
        self.discount = discount  # Lưu giá trị hệ số chiết khấu tương lai (gamma).
        self.iterations = iterations  # Lưu số lượng vòng lặp tối đa chạy Value Iteration.
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()  # Gọi hàm thực thi thuật toán Value Iteration ngay khi khởi tạo Agent.

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        for i in range(self.iterations):  # Vòng lặp chạy qua số lượng K lần lặp cấu hình sẵn.
            # Tạo "thùng chứa tạm". util.Counter() hoạt động như một Dictionary mặc định giá trị 0
            new_values = util.Counter()   # Khởi tạo bảng giá trị tạm thời cho lượt lặp hiện tại để tránh ghi đè dữ liệu đang tính.
            
            for state in self.mdp.getStates():  # Duyệt qua từng trạng thái đang tồn tại trong không gian MDP.
                if self.mdp.isTerminal(state):  # Kiểm tra xem trạng thái đang xét có phải trạng thái kết thúc hay không.
                    new_values[state] = 0       # Nếu là Terminal State thì giá trị nhận được cố định bằng 0.
                    continue                    # Bỏ qua phần tính toán phía dưới và nhảy sang trạng thái tiếp theo.
                
                # Tìm max Q-value cho trạng thái này
                best_action = self.computeActionFromValues(state)  # Tìm hành động mang lại giá trị kỳ vọng lớn nhất dựa trên bảng giá trị cũ.
                if best_action is not None:  # Nếu tồn tại hành động hợp lệ từ trạng thái hiện tại.
                    new_values[state] = self.computeQValueFromValues(state, best_action)  # Gán giá trị trạng thái mới bằng Q-value lớn nhất vừa tìm được.
            
            # Cập nhật hàng loạt (Batch update)
            self.values = new_values  # Gán toàn bộ bảng giá trị đồng bộ tạm thời vào bảng giá trị chính sau khi kết thúc một lượt lặp.

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]  # Trả về giá trị của trạng thái truyền vào từ bảng dữ liệu self.values.


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        q_value = 0  # Khởi tạo giá trị Q-value ban đầu bằng 0.
        # Duyệt qua các trạng thái tiếp theo có thể xảy ra và xác suất của chúng
        for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):  # Lấy danh sách các cặp (trạng thái đích, xác suất xảy ra dịch chuyển).
            reward = self.mdp.getReward(state, action, nextState)  # Lấy giá trị phần thưởng tức thì khi thực hiện hành động chuyển sang trạng thái mới.
            # Áp dụng phương trình Bellman: nhân xác suất với tổng phần thưởng tức thì và giá trị chiết khấu tương lai.
            q_value += prob * (reward + self.discount * self.values[nextState])  
        return q_value  # Trả về tổng giá trị Q-value kỳ vọng tích lũy được.

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):  # Kiểm tra nếu trạng thái hiện tại là đích/kết thúc trò chơi.
            return None                 # Trạng thái kết thúc không có hành động hợp lệ tiếp theo nên trả về None.
            
        best_action = None          # Khởi tạo biến lưu hành động tối ưu nhất là rỗng.
        max_q = float('-inf') # Khởi tạo giá trị lớn nhất bằng âm vô cùng
        
        for action in self.mdp.getPossibleActions(state):  # Lặp qua tất cả các hành động hợp lệ mà Agent có thể thực hiện từ trạng thái này.
            q_value = self.computeQValueFromValues(state, action)  # Tính toán giá trị Q-value ứng với hành động hiện tại đang xét.
            if q_value > max_q:         # So sánh nếu Q-value vừa tính lớn hơn giá trị cực đại tạm thời đã lưu.
                max_q = q_value         # Cập nhật lại giá trị cực đại mới.
                best_action = action    # Cập nhật hành động tối ưu tương ứng với giá trị cực đại đó.
                
        return best_action  # Trả về hành động mang lại lợi ích kinh tế (Q-value) cao nhất.

    def getPolicy(self, state):
        return self.computeActionFromValues(state)  # Trả về hành động tối ưu dựa vào hàm tính toán chính sách.

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)  # Lấy hành động tối ưu trực tiếp từ hàm chính sách mà không thêm yếu tố ngẫu nhiên.

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)  # Gọi hàm và trả về giá trị Q-value cho cặp trạng thái và hành động cụ thể.


class PrioritizedSweepingValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta  # Lưu ngưỡng sai số tối thiểu (theta) để quyết định xem có cập nhật phần tử vào hàng đợi hay không.
        ValueIterationAgent.__init__(self, mdp, discount, iterations)  # Kế thừa và gọi hàm khởi tạo của lớp cha ValueIterationAgent.

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # Bước 1: Tính toán tiền bối (Predecessors) của tất cả các trạng thái
        predecessors = {}  # Tạo một từ điển rỗng để lưu tập hợp các trạng thái tiền bối cho từng trạng thái.
        for state in self.mdp.getStates():  # Duyệt toàn bộ các trạng thái có trong môi trường.
            predecessors[state] = set()     # Khởi tạo một tập hợp (set) rỗng cho từng trạng thái để tránh trùng lặp tiền bối.
            
        for state in self.mdp.getStates():  # Tiếp tục duyệt để tìm mối quan hệ dịch chuyển giữa các trạng thái.
            if not self.mdp.isTerminal(state):  # Chỉ xét các trạng thái không phải terminal vì terminal không thể thực hiện hành động đi đâu tiếp.
                for action in self.mdp.getPossibleActions(state):  # Lặp qua các hành động hợp lệ từ trạng thái hiện tại.
                    for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):  # Lấy các trạng thái đích có thể đến.
                        if prob > 0:  # Nếu xác suất dịch chuyển sang trạng thái đích lớn hơn 0.
                            predecessors[nextState].add(state)  # Thêm trạng thái hiện tại vào danh sách tiền bối của trạng thái đích (nextState).

        # Bước 2: Khởi tạo Hàng đợi ưu tiên (Priority Queue)
        pq = util.PriorityQueue()  # Khởi tạo đối tượng hàng đợi ưu tiên từ thư viện util.
        
        for state in self.mdp.getStates():  # Duyệt qua từng trạng thái để tính toán độ ưu tiên ban đầu.
            if not self.mdp.isTerminal(state):  # Bỏ qua trạng thái kết thúc vì giá trị của nó luôn cố định bằng 0.
                # Tìm giá trị Q lớn nhất (max Q-value) cho trạng thái hiện tại
                max_q = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])  # Tính giá trị Q-value lớn nhất có thể đạt được từ trạng thái này.
                # Tính sai số (diff)
                diff = abs(self.values[state] - max_q)  # Đo lường sự chênh lệch (sai số tuyệt đối) giữa giá trị hiện tại lưu trữ và giá trị tối ưu tính theo Bellman.
                # Đưa vào hàng đợi với mức độ ưu tiên là -diff (vì đây là min-heap)
                pq.push(state, -diff)  # Đưa trạng thái vào hàng đợi với độ ưu tiên âm (giá trị diff càng lớn thì -diff càng nhỏ, do min-heap ưu tiên giá trị nhỏ nhất nên trạng thái có sai số lớn nhất sẽ được lấy ra trước).

        # Bước 3: Vòng lặp cập nhật ưu tiên
        for i in range(self.iterations):  # Chạy vòng lặp giới hạn bởi số lần lặp iterations tối đa cấu hình sẵn.
            if pq.isEmpty():  # Kiểm tra điều kiện dừng sớm nếu hàng đợi rỗng hoàn toàn trước khi hết lượt lặp.
                break         # Thoát khỏi vòng lặp tính toán giá trị.
                
            # Lấy trạng thái có sai số lớn nhất ra khỏi hàng đợi
            state = pq.pop()  # Rút trạng thái có độ ưu tiên cao nhất (sai số lớn nhất) ra khỏi hàng đợi để xử lý.
            
            # Cập nhật giá trị của trạng thái đó (không dùng thùng chứa tạm như Q1 nữa)
            if not self.mdp.isTerminal(state):  # Nếu trạng thái lấy ra không phải terminal state.
                max_q = max([self.computeQValueFromValues(state, action) for action in self.mdp.getPossibleActions(state)])  # Tính lại giá trị max Q-value chính xác ở thời điểm hiện tại.
                self.values[state] = max_q  # Thay thế và cập nhật trực tiếp giá trị mới này vào bảng lưu trữ chính self.values.
                
            # Cập nhật các tiền bối của trạng thái vừa được xử lý
            for p in predecessors[state]:  # Duyệt qua tất cả các trạng thái tiền bối (đứng trước) của trạng thái vừa cập nhật.
                if not self.mdp.isTerminal(p):  # Chỉ cập nhật các trạng thái tiền bối nếu nó không phải là terminal.
                    max_q_p = max([self.computeQValueFromValues(p, action) for action in self.mdp.getPossibleActions(p)])  # Tính toán max Q-value mới cho trạng thái tiền bối p.
                    diff_p = abs(self.values[p] - max_q_p)  # Tính sai số tuyệt đối hiện tại của trạng thái tiền bối p.
                    # Nếu sai số của tiền bối lớn hơn ngưỡng theta, cập nhật nó trong hàng đợi
                    if diff_p > self.theta:  # So sánh sai số vừa tính với ngưỡng sai số tối thiểu cho phép (theta).
                        pq.update(p, -diff_p)  # Cập nhật hoặc chèn trạng thái tiền bối p vào hàng đợi với độ ưu tiên mới là -diff_p.