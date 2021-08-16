import requests
import json
import urllib3
import socket
import time

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
        # Test connectivity
        try:
            res = requests.post(url=self.url+"/lift/status/motion_mode", headers=self.header, json=self.data, timeout=1.0)
            res.raise_for_status()
            return True
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print(f"Connection Error: {e}")
            return False

    def get_lift_available_floor(self):
        try:
            response = requests.post(url=self.url+"/lift/status/available_floor", headers=self.header, json=self.data, timeout=1.0) 
            if response:
                current_location = response.json().get("body").get("available_floor")
                return current_location
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
    
    def get_lift_motion_mode(self):
        try:
            response = requests.post(url=self.url+"/lift/status/motion_mode", headers=self.header, json=self.data, timeout=1.0) 
            if response:
                motion = response.json().get("body").get("motion")
                if motion is None:
                    return 3
                elif motion == "Stopped":
                    return 0
                elif motion == "Up":
                    return 1
                elif motion == "Down":
                    return 2
            else:
                return 4
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return 4 

    def get_lift_destination(self):
        try:
            response = requests.post(url=self.url+"/lift/status/destination", headers=self.header, json=self.data, timeout=1.0) 
            if response:
                destination = response.json().get("body").get("destination")
                return destination
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return "UNKNOWN"

    def get_lift_current_location(self):
        try:
            response = requests.post(url=self.url+"/lift/status/current_location", headers=self.header, json=self.data, timeout=1.0) 
            if response:
                current_location = response.json().get("body").get("current_location")
                return current_location
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return "UNKNOWN"

    def get_lift_door_mode(self):
        try:
            response = requests.post(url=self.url+"/lift/status/door_status", headers=self.header, json=self.data, timeout=1.0) 
            if response:
                door_mode = response.json().get("body").get("door_state")
                if door_mode is None:
                    return 3
                elif door_mode == "Stopped":
                    return 0
                elif door_mode == "Up":
                    return 1
                elif door_mode == "Down":
                    return 2
            else:
                return 4
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return 4 

    def lift_request_command(self, floor_request):
        # TODO:need to understand more on how passing data to Lift API
        print(floor_request)
        try:
            response = requests.post(url=self.url+"/lift/request_floorlevel",headers=self.header, json=self.data, timeout=1.0)
            if response:
                result = response.json()["body"]
                if (result.get("result") is not None):
                    return True
                else:
                    print("Lift door request is unsuccessful")
                    return False
            else:
                print("Invalid response received")
                return False
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return False

    def open_lift_door(self):
        try:
            response = requests.post(url=self.url+"/lift/door/remoteopen",headers=self.header, json=self.data, timeout=1.0)
            if response:
                result = response.json()["body"]
                if (result.get("result") is not None):
                    return True
                else:
                    print("Lift door could not perform open")
                    return False
            else:
                print("Invalid response received")
                return False
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return False

    def close_lift_door(self):
        try:
            response = requests.post(url=self.url+"/lift/door/remoteclose",headers=self.header, json=self.data, timeout=1.0)
            if response:
                result = response.json()["body"]
                if (result.get("result") is not None):
                    return True
                else:
                    print("lift door could not perform close")
                    return False
            else:
                print("Invalid response received")
                return False
        except (socket.gaierror, urllib3.exceptions.NewConnectionError, urllib3.exceptions.MaxRetryError, requests.exceptions.HTTPError ,requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            print("Connection Error. "+str(e))
            return False