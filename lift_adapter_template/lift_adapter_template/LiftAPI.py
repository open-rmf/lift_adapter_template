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

import sys
import enum
from yaml import YAMLObject
from __future__ import annotations
from rclpy.impl.rcutils_logger import RcutilsLogger


class DoorState(enum.IntEnum):
    CLOSED = 0
    MOVING = 1
    OPEN = 2


class MotionState(enum.IntEnum):
    STOPPED = 0
    UP = 1
    DOWN = 2
    UNKNOWN = 3


'''
    The LiftAPI class is a wrapper for API calls to the lift. Here users are
    expected to fill up the implementations of functions which will be used by
    the LiftAdapter. For example, if your lift has a REST API, you will need to
    make http request calls to the appropriate endpints within these functions.
'''
class LiftAPI:
    # The constructor accepts a safe loaded YAMLObject, which should contain all
    # information that is required to run any of these API calls.
    def __init__(self, config: YAMLObject, logger: RcutilsLogger):
        self.config = config
        self.logger = logger

        # Test initial connectivity
        self.logger.info('Checking connectivity.')
        if not self.check_connection():
            self.logger.error('Failed to establish connection with lift API')
            sys.exit(1)

    def check_connection(self) -> bool:
        ''' Return True if connection to the lift is successful'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return True

    def available_floors(self) -> list[str]:
        ''' Returns the available floors for this lift'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return []

    def current_floor(self) -> str:
        ''' Returns the current floor of this lift'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return ''

    def destination_floor(self) -> str:
        ''' Returns the destination floor of this lift'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return ''

    def lift_door_state(self) -> DoorState:
        ''' Returns the state of the lift door'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return DoorState.CLOSED

    def lift_motion_state(self) -> MotionState:
        ''' Returns the lift cabin motion state'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return MotionState.UNKNOWN

    def command_lift(self, floor: str) -> bool:
        ''' Sends the lift cabin to a specific floor and opens all available
            doors for that floor. Returns True if the request was sent out
            successfully, False otherwise'''
        # ------------------------ #
        # IMPLEMENT YOUR CODE HERE #
        # ------------------------ #
        return False
