#!/usr/bin/env python3

# Copyright 2022 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys
import yaml
from typing import Optional
from yaml import YAMLObject

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rmf_lift_msgs.msg import LiftState, LiftRequest

from .LiftAPI import LiftAPI

'''
    The LiftAdapterTemplate is a node which provide updates to Open-RMF, as well
    as handle incoming requests to control the integrated lift, by calling the
    implemented functions in LiftAPI.
'''
class LiftAdapterTemplate(Node):
    def __init__(self, args, config: YAMLObject):
        super().__init__('lift_adapter_template')

        self.lift_name = args.name
        self.lift_config = config
        self.lift_api = LiftAPI(self.lift_config, self.get_logger())
        self.lift_state = None
        self.lift_request = None

        # Initialize status
        self.get_logger().info('Initializing with status.')
        self.lift_state = self._lift_state()
        if self.lift_state is None:
            self.get_logger().error('Failed initilize lift status.')
            sys.exit(1)
        print(f'Initial state: {self.lift_state}')

        self.lift_state_pub = self.create_publisher(
            LiftState,
            'lift_states',
            qos_profile=qos_profile_system_default)
        self.lift_request_sub = self.create_subscription(
            LiftRequest,
            'lift_requests',
            self.lift_request_callback,
            qos_profile=qos_profile_system_default)
        self.update_timer = self.create_timer(0.5, self.update_callback)
        self.pub_state_timer = self.create_timer(1.0, self.publish_state)
        self.get_logger().info('Running LiftAdapterTemplate')

    def update_callback(self):
        new_state = self._lift_state()
        if new_state is None:
            self.get_logger().error(
                f'Unable to get new state from lift {self.lift_name}')
            return
        self.lift_state = new_state

        # No request to consider
        if self.lift_request is None:
            return

        # If all is done, set self.request to None
        if self.lift_request.destination_floor == \
                self.lift_state.current_floor and \
                self.lift_state.door_state == LiftState.DOOR_OPEN:
            self.lift_request = None

    def _lift_state(self) -> Optional[LiftState]:
        new_state = LiftState()
        new_state.lift_time = self.get_clock().now().to_msg()
        new_state.lift_name = self.lift_name

        def _retrieve_fail_error(value_name: str):
            self.get_logger().error(f'Unable to retrieve {value_name}')
            return None

        available_floors = self.lift_api.available_floors()
        if available_floors is None:
            return _retrieve_fail_error('available_floors')
        new_state.available_floors = [f for f in available_floors]

        current_floor = self.lift_api.current_floor()
        if current_floor is None:
            return _retrieve_fail_error('current_floor')
        new_state.current_floor = current_floor

        destination_floor = self.lift_api.destination_floor()
        if destination_floor is None:
            return _retrieve_fail_error('destination_floor')
        new_state.destination_floor = destination_floor

        door_state = self.lift_api.lift_door_state()
        if door_state is None:
            return _retrieve_fail_error('door_state')
        new_state.door_state = door_state

        motion_state = self.lift_api.lift_motion_state()
        if motion_state is None:
            return _retrieve_fail_error('motion_state')
        new_state.motion_state = motion_state

        new_state.available_modes = [LiftState.MODE_HUMAN, LiftState.MODE_AGV]
        new_state.current_mode = LiftState.MODE_AGV

        if self.lift_request is not None:
            if self.lift_request.request_type == \
                    LiftRequest.REQUEST_END_SESSION:
                new_state.session_id = ''
            else:
                new_state.session_id = self.lift_request.session_id
        return new_state

    def publish_state(self):
        if self.lift_state is None:
            self.get_logger().info('No lift state received.')
            return
        self.lift_state_pub.publish(self.lift_state)

    def lift_request_callback(self, msg):
        if msg.lift_name != self.lift_name:
            return

        if self.lift_request is not None:
            self.get_logger().info(
                'Lift is currently busy with another request, try again later.')
            return

        if self.lift_state is not None and \
                msg.destination_floor not in self.lift_state.available_floors:
            self.get_logger().info(
                'Floor {} not available.'.format(msg.destination_floor))
            return

        if not self.lift_api.command_lift(msg.destination_floor):
            self.get_logger().error(
                f'Failed to send lift to {msg.destination_floor}.')
            return

        self.get_logger().info(f'Requested lift to {msg.destination_floor}.')
        self.lift_request = msg


def main(argv=sys.argv):
    args_without_ros = rclpy.utilities.remove_ros_args(argv)
    parser = argparse.ArgumentParser(
        prog='lift_adapter_template',
        description='Lift adapter template')
    parser.add_argument('-n', '--name', required=True, type=str)
    parser.add_argument('-c', '--config', required=True, type=str)
    args = parser.parse_args(args_without_ros[1:])

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    rclpy.init()
    node = LiftAdapterTemplate(args, config)
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
