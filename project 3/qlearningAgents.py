# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qValues = Counter()  # Khởi tạo một đối tượng Counter (bản chất là Dict) dùng để lưu giữ các giá trị Q(state, action), mặc định nếu chưa thấy sẽ trả về 0.


    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.qValues[(state, action)]  # Truy vấn trực tiếp vào Counter với khóa là tuple (state, action) để lấy giá trị Q-value tương ứng.


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)  # Lấy danh sách các hành động hợp lệ mà Agent có thể làm từ trạng thái hiện tại.
        if not legalActions:  # Nếu danh sách hành động trống (ví dụ như ở trạng thái kết thúc/Terminal State).
            return 0          # Trả về giá trị mặc định là 0 theo đúng yêu cầu đề bài.
        maxQValue = float('-inf')  # Khởi tạo giá trị Q lớn nhất bằng âm vô cùng để phục vụ việc tìm kiếm cực đại.
        for action in legalActions:  # Duyệt qua từng hành động hợp lệ trong danh sách.
            actionQValue = self.getQValue(state, action)  # Lấy giá trị Q-value tương ứng với cặp trạng thái và hành động hiện tại.
            if actionQValue > maxQValue:  # Nếu tìm thấy giá trị Q lớn hơn giá trị cực đại tạm thời.
                maxQValue = actionQValue  # Cập nhật giá trị cực đại mới bằng giá trị Q vừa tìm thấy.

        return maxQValue  # Trả về giá trị Q-value lớn nhất của trạng thái hiện tại.


    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)  # Thu thập toàn bộ các hành động hợp pháp tại trạng thái hiện tại.
        if not legalActions:  # Nếu không có hành động nào khả thi (Terminal State).
            return None       # Trả về None báo hiệu không có hành động hợp lệ.
        bestAction = None         # Khởi tạo biến lưu hành động tốt nhất là rỗng.
        maxQValue = float('-inf') # Khởi tạo giá trị Q lớn nhất bằng âm vô cùng.
        for action in legalActions:  # Duyệt vòng lặp qua từng hành động trong danh sách hành động hợp pháp.
            actionQValue = self.getQValue(state, action)  # Lấy giá trị Q-value từ bảng lưu trữ dựa trên hành động đang xét.
            if actionQValue > maxQValue:  # Nếu giá trị Q-value của hành động này vượt qua giá trị lớn nhất hiện tại.
                maxQValue = actionQValue  # Cập nhật mốc giá trị lớn nhất mới.
                bestAction = action       # Ghi nhận hành động này tạm thời là tốt nhất.

        return bestAction  # Trả về hành động mang lại giá trị Q-value tối ưu nhất cho Agent.


    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)  # Lấy danh sách các hành động có thể thực hiện.
        action = None                               # Khởi tạo biến lưu hành động trả về cuối cùng bằng None.
        "*** YOUR CODE HERE ***"
        if not legalActions:  # Nếu không tồn tại hành động nào hợp lệ từ vị trí này.
            return action     # Trả về kết quả ban đầu là None ngay lập tức.
        if util.flipCoin(self.epsilon):  # Sử dụng thuật toán lật đồng xu với xác suất bằng epsilon để quyết định xem có hành vi khám phá (exploration) hay không.
            return random.choice(legalActions)  # Nếu trúng (True), chọn ngẫu nhiên một hành động trong danh sách hành động hợp lệ để khám phá môi trường.
        
        return self.computeActionFromQValues(state)  # Nếu trượt (False), Agent thực hiện hành vi khai thác (exploitation) bằng cách chọn hành động tối ưu nhất theo chính sách hiện tại.


    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        currentQValue = self.qValues[(state, action)]  # Lấy giá trị Q-value hiện tại của cặp (state, action) trước khi cập nhật.
        sample = reward + self.discount * self.computeValueFromQValues(nextState)  # Tính toán giá trị mẫu thử (Sample) dựa theo công thức: phần thưởng nhận được cộng với giá trị chiết khấu tương lai lớn nhất từ trạng thái tiếp theo.
        self.qValues[(state, action)] = (1 - self.alpha) * currentQValue + self.alpha * sample  # Áp dụng công thức cập nhật Q-learning trọng số động (Temporal Difference update) phối hợp giữa giá trị cũ và mẫu thử mới thông qua hệ số học alpha.


    def getPolicy(self, state):
        return self.computeActionFromQValues(state)  # Trả về hành động tối ưu cho trạng thái được yêu cầu theo chính sách.

    def getValue(self, state):
        return self.computeValueFromQValues(state)  # Trả về giá trị trạng thái tối ưu (max Q-value) được tính toán.


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon      # Gán giá trị tham số epsilon (khám phá) vào từ điển args.
        args['gamma'] = gamma          # Gán giá trị tham số gamma (chiết khấu) vào từ điển args.
        args['alpha'] = alpha          # Gán giá trị tham số alpha (tốc độ học) vào từ điển args.
        args['numTraining'] = numTraining  # Gán số lượng trận đấu huấn luyện vào hệ thống.
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)  # Gọi hàm khởi tạo của lớp cha QLearningAgent với các tham số đã đóng gói.

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)  # Gọi phương thức lấy hành động từ lớp cha QLearningAgent.
        self.doAction(state,action)                     # Thông báo và thực hiện hành động đã chọn lên giao diện/môi trường game Pacman.
        return action  # Trả về hành động cuối cùng được thực thi.


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()  # Tìm kiếm và khởi tạo bộ trích xuất đặc trưng (Feature Extractor) tương ứng từ chuỗi tên truyền vào.
        PacmanQAgent.__init__(self, **args)  # Khởi tạo các thuộc tính cơ bản của PacmanQAgent.
        self.weights = util.Counter()  # Khởi tạo một đối tượng Counter để lưu trữ trọng số tương ứng với mỗi đặc trưng (Feature) học được.

    def getWeights(self):
        return self.weights  # Trả về bảng trọng số hiện tại của mô hình xấp xỉ hàm tuyến tính.

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # Đoạn code hoàn chỉnh cho phần này (nếu bạn cần bổ sung giải pháp tự động):
        # features = self.featExtractor.getFeatures(state, action)  # Lấy danh sách đặc trưng từ cặp trạng thái và hành động.
        # return self.weights * features                             # Tính toán tích vô hướng (dot product) giữa vector trọng số và vector đặc trưng để sinh ra giá trị Q-value.
        util.raiseNotDefined()  # Hàm mẫu mặc định ném ra ngoại lệ nếu chưa được viết đè, bạn có thể thay thế bằng 2 dòng comment phía trên.

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # Đoạn code hoàn chỉnh cho phần này (nếu bạn cần bổ sung giải pháp tự động):
        # difference = (reward + self.discount * self.computeValueFromQValues(nextState)) - self.getQValue(state, action) # Tính sai số Temporal Difference (TD error).
        # features = self.featExtractor.getFeatures(state, action)  # Trích xuất vector đặc trưng tại thời điểm hiện tại.
        # for feature in features:                                  # Duyệt qua từng đặc trưng xuất hiện.
        #     self.weights[feature] += self.alpha * difference * features[feature] # Cập nhật trọng số của từng đặc trưng theo hướng giảm thiểu sai số.
        util.raiseNotDefined()  # Hàm mẫu mặc định ném ra ngoại lệ nếu chưa được viết đè.

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)  # Gọi hàm xử lý kết thúc game từ lớp cha PacmanQAgent để cập nhật số trận đấu đã qua.

        # did we finish training?
        if self.episodesSoFar == self.numTraining:  # Kiểm tra xem tổng số trận đã chơi thực tế đã đạt tới giới hạn huấn luyện chưa.
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass  # Giữ chỗ trống, bạn có thể in bảng trọng số `print self.weights` tại đây nếu cần debug mô hình khi kết thúc huấn luyện.