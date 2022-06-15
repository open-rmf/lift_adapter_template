from pickletools import string1
from tokenize import Number
import requests
import json
import urllib3
import socket
import time
from rmf_lift_msgs.msg import LiftState

class LiftClientAPI:
    def __init__(self,url,api_key,api_value,lift_id):
        self.url = url
        self.header = {api_key:api_value}
        self.data = {"id": lift_id}

        count = 0
        self.connected = True
        while not self.check_connection():
            if count >= 5:
                print("Unable to connect to lift client API.")
                self.connected = False
                break
            else:
                print("Unable to connect to lift client API. Attempting to reconnect...")
                count += 1
            time.sleep(1)

    def check_connection(self):
        ''' Return True if connection to the lift API server is successful'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return False

    def open_lift_door(self):
        ''' Return True if the lift API server successfully receives the open lift door command'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return False

    def close_lift_door(self):
        ''' Return True if the lift API server successfully receives the close lift door command'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return False

    def command_lift_to_floor(self, floor_request):
        # TODO:need to understand more on how passing data to Lift API
        ''' Return True if the lift API server successfully receives the lift floor command'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return False

    def get_lift_door_mode(self):
        ''' Return the lift door state with reference rmf_lift_msgs::LiftState. 
            Return LiftState.DOOR_CLOSED when lift door state is closed.
            Return LiftState.DOOR_MOVING when lift door state is moving.
            Return LiftState.DOOR_OPEN when lift door state is open.'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return LiftState.DOOR_CLOSED

    def get_lift_motion_mode(self):
        ''' Return the lift motion state with reference rmf_lift_msgs::LiftState. 
            Return LiftState.MOTION_STOPPED when lift is motionless.
            Return LiftState.MOTION_UP when the lift is moving upwards.
            Return LiftState.MOTION_DOWN when lift is moving downwards.
            Return LiftState.MOTION_UNKNOWN when lift motion state is unknown.'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return LiftState.MOTION_STOPPED

    def get_lift_available_floors(self):
        ''' Return list of available floors for this lift to be commanded to.'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return []

    def get_lift_current_floor(self):
        ''' Return the current floor that the lift is on.'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return ''

    def get_lift_destination_floor(self):
        ''' Return the destination floor of the lift.'''
        ## ------------------------ ##
        ## IMPLEMENT YOUR CODE HERE ##
        ## ------------------------ ##
        return ''
