# running this for 2 hours yielded - 15seconds
# cloned and ran this for another 4 hours yielded no significant improvement in time but the completion rate was very high.

import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
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

    # Initialize the reward with typical value
    reward = 10.0
    max_speed = 3
    
    speed_ratio = round((speed / max_speed * 100),2)

    if not all_wheels_on_track:
        reward = reward - 1
    
    if is_crashed:
        reward = -10
        
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
    
    # Give higher reward if the car is away from border
    if distance_from_center <= marker_3:
        reward = reward - 1

    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff

    # Penalize the reward if the difference is too large
    DIRECTION_THRESHOLD = 120.0
    if direction_diff > DIRECTION_THRESHOLD:
        reward = reward - 2

    
    if (direction_diff < 10) and (speed_ratio > 0.9):
        reward = reward + 10
    if (direction_diff > 10) and (direction_diff < 90) and (speed_ratio < 0.3):
        reward = reward + 10
    if (direction_diff < 5) and (speed_ratio > 0.95):
        reward = reward + 10
    
    # Read input variable
    steps = params['steps']
    progress = params['progress']

    # Total num of steps we want the car to finish the lap, it will vary depends on the track length
    TOTAL_NUM_STEPS = 300

    # Initialize the reward with typical value
    reward = 1.0

    # Give additional reward if the car pass every 100 steps faster than expected
    if (steps % 100) == 0 and progress > (steps / TOTAL_NUM_STEPS) * 100 :
        reward += 10.0

    return float(reward)
