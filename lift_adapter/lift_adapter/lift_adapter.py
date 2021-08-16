import sys
import math
import yaml
import argparse

import socket
import urllib3
import time
import threading

import rclpy
from lift_adapter.LiftClientAPI import LiftClientAPI
from rclpy.node import Node
from rclpy.time import Time
from rmf_lift_msgs.msg import LiftRequest, LiftState

###############################################################################

class LiftAdapter(Node):
    def __init__(self,config_yaml):
        super().__init__('lift_adapter')
        self.get_logger().info('Starting lift adapter...')

        # Get value from config file
        self.lift_name = config_yaml['lift']['name']
        url = config_yaml['lift']['api_endpoint']
        api_key = config_yaml['lift']['header_key']
        api_value = config_yaml['lift']['header_value']
        lift_id = config_yaml['lift']['lift_id']

        self.api = LiftClientAPI(url,api_key,api_value,lift_id)
        assert self.api.connected, "Unable to establish connection with lift"

        # The available_floors need to passing from either config file or API/Lift Software
        self.available_floors = self.api.get_lift_available_floor()
        # The floor that the lift currently at, need to get this info from API/Lift Software
        self.current_floor = ''
        # The floor that the lift is going to, need to get this info from API/Lift Software
        self.destination_floor = ''
        # default the lift door is close, this info needs to be provided by API/Lift Software
        self.lift_door_state = 0
        # default the motion of the lift is stopped, this info needs to be provided by API/Lift Software
        self.lift_motion_state = 0
        self.floor_request = ''
        # current requestion id, requestor_id(session_id) from the LiftRequest
        # after the lift request task completed, the value will be remove from the variable self.current_requestor
        # TODO: to write a logic to remove current_requestor value after the lift request completed
        self.current_requestor = ''

        self.lift_states_pub = self.create_publisher(
            LiftState, 'lift_states', 1)

        self.lift_request_sub = self.create_subscription(
            LiftRequest, 'adapter_lift_requests', self.lift_request_cb, 1)

        self.periodic_timer = self.create_timer(
            1.0, self.time_cb)

    def time_cb(self):
        self.get_lift_status()

        state_msg = LiftState()
        state_msg.lift_time = self.get_clock().now().to_msg()

        # publish states of the lift
        state_msg.lift_name = self.lift_name
        state_msg.available_floors = self.available_floors
        state_msg.current_floor = self.current_floor
        state_msg.destination_floor = self.destination_floor
        state_msg.door_state = self.lift_door_state
        state_msg.motion_state = self.lift_motion_state
        # default available_lift mode to AGV only
        # TODO: to understand how to get the lift mode
        state_msg.available_modes = [1,2]
        state_msg.current_mode = LiftState.MODE_AGV
        state_msg.session_id = self.current_requestor
        self.lift_states_pub.publish(state_msg)

    def get_lift_status(self):
        # Get lift status directly from Lift API/Software
        self.current_floor = self.api.get_lift_current_location()
        self.available_floors = self.api.get_lift_available_floor()
        self.destination_floor = self.api.get_lift_destination()
        self.lift_door_state = self.api.get_lift_door_mode()
        self.lift_motion_state = self.get_lift_motion_mode()

    def lift_request_cb(self, msg: LiftRequest):
        if msg.lift_name == self.lift_name:
            self.get_logger().info(f"lift request [{msg.destination_floor.value}] requested by {msg.session_id}")
            self.floor_request = msg.destination_floor.value
            self.current_requestor = msg.session_id.value
            # AGV Mode
            if msg.request_type.value == 1:
                self.execute_agv_mode_request()
            elif msg.request_type.value == 2:
                self.execute_human_mode_request(msg.door_state.value)
                
    def execute_agv_mode_request(self):
        # Door requests are not necessary in "AGV" mode, when the doors are always held open when the lift cabin is stopped
        self.get_logger().info('executing Lift Request in AGV Mode')
        success = self.api.lift_request_command(self.floor_request)
        # call the lift until lift API give success feedback
        while not success:
            success = self.api.lift_request_command(self.floor_request)
            if success:
                self.get_logger().info(f"Request to lift [{self.lift_name}] to floor [{self.floor_request}] is successful")
            else:
                self.get_logger().warning(f"Request to lift [{self.lift_name}] to floor [{self.floor_request}] is unsuccessful")
            time.sleep(2)


    def execute_human_mode_request(self,door_request):
        # door requests are necessary in "human" mode to open/close doors
        self.get_logger().info('executing Lift Request in Human Mode')
        # call the lift until lift API give success feedback
        success = False
        while not success:
            success = self.api.lift_request_command(self.floor_request)
            if success:
                self.get_logger().info(f"Request to lift [{self.lift_name}] to floor [{self.floor_request}] is successful")
            else:
                self.get_logger().warning(f"Request to lift [{self.lift_name}] to floor [{self.floor_request}] is unsuccessful")
            time.sleep(2)

        while not door_request == self.current_floor:
            self.get_logger().info(f"Waiting lift to reach floor [{self.door_request}]")
            time.sleep(1)
        
        success = False
        while not success:
            if door_request == 0:
                success = self.api.open_lift_door()
                lift_door_cmd = 'Close'
            else:
                success = self.api.close_lift_door()
                lift_door_cmd = 'Open'

            if success:
                self.get_logger().info(f"Request [{self.lift_name}] door to [{lift_door_cmd}] is successful")
            else:
                self.get_logger().warning(f"Request [{self.lift_name}] door to [{lift_door_cmd}] is unsuccessful")
            time.sleep(3.0)

###############################################################################

def main(argv=sys.argv):
    rclpy.init(args=argv)

    args_without_ros = rclpy.utilities.remove_ros_args(argv)
    parser = argparse.ArgumentParser(
        prog="lift_adapter",
        description="Configure and spin up lift adapter for physical lift ")
    parser.add_argument("-c", "--config_file", type=str, required=True,
                        help="Path to the config.yaml file for this lift adapter")
    args = parser.parse_args(args_without_ros[1:])
    config_path = args.config_file

    # Load config and nav graph yamls
    with open(config_path, "r") as f:
        config_yaml = yaml.safe_load(f)

    lift_adapter = LiftAdapter(config_yaml)
    rclpy.spin(lift_adapter)

    lift_adapter.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main(sys.argv)