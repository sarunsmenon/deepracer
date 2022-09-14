
# running this for 2 hours yielded - 15seconds
# cloned and ran this for another 4 hours yielded no significant improvement in time but the completion rate was very high.

import math


def direction(wp_1, wp_2, heading):
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(wp_1[1] - wp_2[1], wp_1[0] - wp_2[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    return direction_diff

def findPoint(wp, current_ind, steps):
    if (current_ind+steps) > (len(wp)-1) :
        look_ahead_point = wp[len(wp)-1]
    else:
        look_ahead_point = wp[current_ind+steps]
    
    return look_ahead_point
    
    
def reward_function(params):
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    
    is_offtrack = params['is_offtrack']
    all_wheels_on_track = params['all_wheels_on_track']
    is_crashed = params['is_crashed']
    speed = params['speed']

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    steering = abs(params['steering_angle']) # We don't care whether it is left or right steering


    # Initialize the reward with typical value
    reward = 10.0
    max_speed = 4
    
    look_ahead_steps_far = int(12)
    look_ahead_steps = int(8)
    look_ahead_steps_near = int(4)
    
    speed_ratio = round((speed / max_speed * 100),2)
    
    dir_threshold = 10

    if not all_wheels_on_track:
        reward = reward - 10
      
    #if off-track penalise
    if is_offtrack:
        reward = reward - 100
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is away from border
    if distance_from_center <= marker_3:
        reward = reward - 10

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    
    current_indices = closest_waypoints[1]-1
    current_point = waypoints[current_indices]
    
        
    look_ahead_point = findPoint(waypoints,current_indices, look_ahead_steps)
    look_ahead_far_point = findPoint(waypoints,current_indices, look_ahead_steps_far)
    look_ahead_near_point = findPoint(waypoints,current_indices,look_ahead_steps_near)
    
    direction_diff = direction(look_ahead_point, current_point, heading)
    direction_far = direction(look_ahead_far_point, current_point, heading)
    direction_near = direction(look_ahead_near_point, current_point, heading)
    
    if (direction_far+dir_threshold > direction_diff) and (direction_diff+dir_threshold > direction_near) and (speed_ratio < 0.2):
        reward = reward + 5000
    elif (direction_far == direction_diff) and (direction_diff == direction_near) and (speed_ratio >= 1):
        reward = reward + 5000
    elif (direction_far+dir_threshold > direction_diff) and (direction_diff+dir_threshold > direction_near) and (steering > 25) and (speed_ratio < 0.2):
        reward = reward + 5000
    elif (direction_diff < direction_far+dir_threshold) and (speed_ratio > 0.2):
        reward = reward + 500
    elif (direction_diff < dir_threshold) and (speed_ratio > 0.9):
        reward = reward + 500
    elif (direction_diff > dir_threshold) and (direction_diff < 90) and (speed_ratio < 0.3):
        reward = reward + 50
    elif (direction_diff < 5) and (speed_ratio > 0.95):
        reward = reward + 200
    
    return float(reward)
