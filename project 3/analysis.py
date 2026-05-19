# analysis.py
# -----------
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


######################
# ANALYSIS QUESTIONS #
######################

# Set the given parameters to obtain the specified policies through
# value iteration.

def question2():
    answerDiscount = 0.9  # Đặt discount gần bằng 1 để Agent quan tâm đến phần thưởng dài hạn (băng qua cầu).
    answerNoise = 0.0     # Đặt noise bằng 0 để Agent di chuyển chính xác 100%, không sợ bị rơi khỏi cầu do ngẫu nhiên.
    return answerDiscount, answerNoise

def question3a():
    answerDiscount = 0.1      # Discount thấp khiến Agent thích phần thưởng gần hơn để tối ưu hóa giá trị tức thời.
    answerNoise = 0.0         # Noise bằng 0 giúp di chuyển an toàn tuyệt đối mà không sợ vô tình trượt chân vào ô nguy hiểm.
    answerLivingReward = 0.0  # Phạt sống bằng 0 (hoặc không thưởng) giúp Agent muốn kết thúc trò chơi nhanh ở ô +1 gần nhất.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3b():
    answerDiscount = 0.3      # Giảm nhẹ discount để Agent vẫn muốn chọn đường ngắn hơn (ô +1) nhưng cần cẩn thận hơn.
    answerNoise = 0.2         # Noise > 0 tạo rủi ro, nhưng vì discount thấp, Agent chọn đi đường vòng qua vách đá để đến ô +1 một cách an toàn.
    answerLivingReward = -0.5 # Sống bị phạt nặng khiến Agent ưu tiên chọn ô +1 gần đó thay vì mạo hiểm đi xa tới ô +10.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3c():
    answerDiscount = 0.9       # Đặt discount cao để phần thưởng xa (+10) giữ được giá trị lớn, hấp dẫn Agent đi quãng đường dài.
    answerNoise = 0.0          # Noise bằng 0 đảm bảo Agent đi dọc hành lang hẹp sát vách đá mà không bao giờ bị rơi.
    answerLivingReward = -0.01 # Phạt sống rất nhẹ để Agent chấp nhận đi đường dài sang phía bên kia bản đồ.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3d():
    answerDiscount = 0.9      # Discount cao giúp Agent nhìn thấy giá trị lớn của ô +10 ở xa.
    answerNoise = 0.2         # Có noise (rủi ro) khiến Agent tránh xa mép vách đá nguy hiểm để bảo toàn mạng sống.
    answerLivingReward = 0.0  # Không phạt sống quá nặng, Agent sẵn sàng đi đường vòng dài an toàn phía trên để tới ô +10.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question3e():
    answerDiscount = 0.9       # Giữ discount cao để tích lũy giá trị nhận được qua thời gian.
    answerNoise = 0.0          # Điểm noise bằng 0 giúp kiểm soát hành vi di chuyển chuẩn xác.
    answerLivingReward = 10.0  # Thưởng sống cực lớn làm Agent muốn sống mãi mãi, né tránh tất cả các ô kết thúc (Terminal states) để liên tục nhận thưởng.
    return answerDiscount, answerNoise, answerLivingReward
    # If not possible, return 'NOT POSSIBLE'

def question7():
    return "NOT POSSIBLE"  # Việc thay đổi tham số Q-learning thông thường không thể ép Agent tối ưu hóa việc đi qua cầu hẹp trong khi liên tục khám phá (Epsilon > 0).
    # If not possible, return 'NOT POSSIBLE'

if __name__ == '__main__':
    print('Answers to analysis questions:')
    import analysis
    for q in [q for q in dir(analysis) if q.startswith('question')]:
        response = getattr(analysis, q)()
        print('  Question %s:\t%s' % (q, str(response)))