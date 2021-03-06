#!/usr/bin/env python
# license removed for brevity

# ROS
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# time mission
import time, sched
import time
import datetime


def movebase_client(target):
    print(target)

    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    # set target location. 
    goal.target_pose.pose.position.x = target[0]
    goal.target_pose.pose.position.y = target[1]
    # set orientation. orientation.w== 1 means face x+
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

def patrol(args):
    print(args)
    try:
        rospy.init_node('movebase_client_py') # initialize only once
        for target in targets: # send goal one by  one
            print("***")
            result = movebase_client(target)
            if result:
                 rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

def time_controller():
    s = sched.scheduler(time.time, time.sleep)
    print('System Bringup Time: '+ datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    s.enter(5,1,patrol,('args',))
    while(1):
        s.run()

if __name__ == '__main__':
    # set target sequence
    # targets=[[5,3], [1,3], [6,-4], [-1,4], [-6,3],[-6,-2],[5,3]] # partrol all room
    targets=[[5,3], [5,4], [5,3]] # partrol test three points
    # begin
    time_controller()


   