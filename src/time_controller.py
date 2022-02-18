#!/usr/bin/env python
# license removed for brevity

# ROS
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# time controller
import datetime
import threading
import time

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

def patrol(targets):
    try:
        rospy.init_node('movebase_client_py') # initialize only once
        for target in targets: # send goal one by  one
            print("***")
            result = movebase_client(target)
            if result:
                 rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")

# always running. execute patrols repeatly with pre-setting interval
def td_patrol_controller(bg_time,end_time, interval, targets):
    while(1):
        time.sleep(interval)
        now_hour= datetime.datetime.now().hour
        now_minute = datetime.datetime.now().minute
        now_second = datetime.datetime.now().second
        now_time= datetime.time(now_hour, now_minute, now_second)
        if now_time> bg_time and now_time <end_time:
            print("[msg from dad] executing patrol at "+ str(now_time))
            patrol(targets)
        else:
            print("[msg from dad] out of time period "+ str(now_time))


if __name__ == '__main__':
    # target sequence
    targets=[[5,3], [1,3], [6,-4], [-1,4], [-6,3],[-6,-2],[5,3]] # partrol all room
    # targets=[[5,3], [5,4], [5,3]] # test case:partrol test two points
     
    # --- set patrol time ---
    # test case, time is fixed
    test_bg_hour= datetime.datetime.now().hour
    test_bg_minute= datetime.datetime.now().minute
    test_bg_second= datetime.datetime.now().second
    bg_time= datetime.time(test_bg_hour, test_bg_minute, test_bg_second)
    end_time= datetime.time(test_bg_hour+ 1, test_bg_minute, test_bg_second)
    interval= 1
    # --- set patrol time ---

    # --- start patrol thread ---
    # patrol controller thread is always running
    thread_patrol_controller= threading.Thread(target= td_patrol_controller(bg_time,end_time, interval, targets))
    thread_patrol_controller.start()
    # --- start patrol thread ---



   