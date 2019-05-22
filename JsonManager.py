# une_variable = "Je suis une variable globale"
#
# def function1():
#     global une_variable
#
#     une_variable = 2
#
#
#
# function1()
# print(une_variable)
#
#
# a = [1,2,3,4,5,6]
# print(a[-1])
#
# import math
#
# throttle = 5
# alpha = 0.5
# total_progress = 0.6
#
# print(throttle/2 - (math.cos(alpha))/2 + 3*total_progress)
#
#
# import math
# #
# # all_x = []
# # all_y = []
# #
# # def reward_function(params):
# #
# #     global all_y
# #     global all_x
# #
# #     MAX_SPEED = 5
# #     reward = 1e-5
# #     is_speed = 0
# #
# #     all_x.append(params["x"])
# #     all_x.append(params["y"])
# #     throttle = params['steering_angle']
# #     x = params["x"]
# #     y = params["y"]
# #     total_progress = params['progress']
# #
# #     distance_from_center = params['distance_from_center']
# #
# #     try:
# #         x_prev = all_x[-2]
# #         y_prev = all_y[-2]
# #     except:
# #         x_prev = x
# #         y_prev = y
# #
# #     alpha = get_alpha(x, y, x_prev, y_prev, distance_from_center)
# #     alpha = 0
# #     print('Alpha = ', alpha)
# #     print('Len All_X', len(all_x))
# #     print('Len All_Y', len(all_y))
# #
# #     track_width = params['track_width']
# #     distance_from_center = params['distance_from_center']
# #
# #     reward = 4.5 * (1 - math.exp(abs(distance_from_center)))
# #
# #     if throttle > 0.9 * MAX_SPEED:
# #         is_speed = 1
# #
# #     reward_cos = throttle * (math.cos(alpha)-max([1-(total_progress/100)-0.2, 0]))
# #     # smooth = throttle * (math.cos(alpha) - 1/(1 + math.exp(-4*(abs(1-(total_progress/100))-0.2))))
# #
# #     reward += reward_cos + is_centered + is_speed
# #
# #     return float(reward)
# #
# # def get_alpha(x, y, x_prev, y_prev, distance_from_center):
# #
# #     res = 0
# #     denominateur = 0
# #     alpha = 0
# #     numerateur = distance_from_center
# #
# #     denominateur = math.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))
# #
# #     if denominateur > 0 and denominateur > numerateur :
# #         res = np.arcsin(numerateur/denominateur)
# #         self.alpha = res
# #         if res == np.NaN :
# #             return 0
# #
# #     return res
# import math
#
# all_x = []
# all_y = []
#
# def reward_function(params):
#
#     global all_y
#     global all_x
#
#     MAX_SPEED = 5
#     reward = 1e-5
#     is_speed = 0
#
#     all_x.append(params["x"])
#     all_x.append(params["y"])
#     throttle = params['steering_angle']
#     x = params["x"]
#     y = params["y"]
#     total_progress = params['progress']
#
#     distance_from_center = params['distance_from_center']
#
#     try:
#         x_prev = all_x[-2]
#         y_prev = all_y[-2]
#     except:
#         x_prev = x
#         y_prev = y
#
#     alpha = get_alpha(x, y, x_prev, y_prev, distance_from_center)
#     alpha = 0
#     print('Alpha = ', alpha)
#
#     track_width = params['track_width']
#     distance_from_center = params['distance_from_center']
#
#
#     reward = -4.54 * abs(distance_from_center) + 1
#
#
#     if throttle < 0.9 * MAX_SPEED:
#         reward *= 0.8
#
#     reward *= throttle/2 - (math.cos(alpha))/2 + 3*total_progress
#
#     return float(reward)
#
# def get_alpha(x, y, x_prev, y_prev, distance_from_center):
#
#     res = 0
#     denominateur = 0
#     alpha = 0
#     numerateur = distance_from_center
#
#     denominateur = math.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))
#
#     if denominateur > 0 and denominateur > numerateur :
#         res = np.arcsin(numerateur/denominateur)
#         self.alpha = res
#         if res == np.NaN :
#             return 0
#
#     return res
import math

a = [1,2,3]

print(math.mean(a))





import math

all_x = []
all_y = []

def reward_function(params):

    global all_y
    global all_x

    MAX_SPEED = 5
    reward = 1e-5
    is_speed = 0

    all_x.append(params["x"])
    all_x.append(params["y"])
    throttle = params['steering_angle']
    x = params["x"]
    y = params["y"]
    total_progress = params['progress']

    distance_from_center = params['distance_from_center']

    try:
        x_prev = all_x[-2]
        y_prev = all_y[-2]
    except:
        x_prev = x
        y_prev = y

    alpha = get_alpha(x, y, x_prev, y_prev, distance_from_center)
    print('Alpha = ', alpha)

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']


    reward = 1.5*(-4.54 * abs(distance_from_center) + 1)


    if throttle < 0.9 * MAX_SPEED:
        reward *= 0.8

    reward *= throttle/2 - (math.cos(alpha))/2 + 3*total_progress

    return float(reward)

def get_alpha(x, y, x_prev, y_prev, distance_from_center):

    res = 0
    denominateur = 0
    alpha = 0
    numerateur = distance_from_center

    denominateur = math.sqrt((x - x_prev) * (x - x_prev) + (y - y_prev) * (y - y_prev))

    if denominateur > 0 and denominateur > numerateur :
        res = np.arcsin(numerateur/denominateur)
        self.alpha = res
        if res == np.NaN :
            return 0

    return res
