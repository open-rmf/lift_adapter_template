# lift_adapter_template

The objective of this package is to serve as a reference or template for writing a python based Open-RMF lift adapter.

> Note: The implementation in this package is not the only way to write a lift adapter. It is only one such example that may be helpful for users to quickly integrate their lifts with RMF.

## Step 1: Fill up missing code
Simply fill up certain blocks of code which make API calls to your lift.

These blocks are highlighted as seen below and are found in `LiftAPI.py`.
```
# IMPLEMENT YOUR CODE HERE #
```

`LiftAPI.py` defines a wrapper for communicating with the lift of interest.
For example, if your lift offers a `REST API` with a `GET` method to obtain the current floor of the lift, then the `LiftAPI::current_floor()` function may be implemented as below

```python
def current_floor(self) -> Optional[str]:
    url = self.prefix + "/data/current_floor" # example endpoint
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return [data['current_floor']]
    except HTTPError as http_err:
        print(f"HTTP error: {http_err}")
    except Exception as err:
        print(f"Other error: {err}")
    return None
```

Alternatively, if your lift offers a websocket port for communication or allows for messages to be exchanged over ROS1/2, then these functions can be implemented using those protocols respectively.

## Step 2: Populate a config.yaml

The `config.yaml` file that is to be passed in via arguments, should contain all the important parameters needed for setting up the LiftAPI. In this template, no example config is provided, the user will need to provide one that has all the information required for the `LiftAPI` to perform its functions.

For example, if the lift API is via REST API calls, one would expect the config file to contain several fields required to perform the requests, and used in the API calls.

```
base_url: "http://192.168.123.123/"
user: "username"
password: "password"
lift_guid: "7e32b6f5-f1ac-14ec-1e1e-94c6911c8a3b"
```

## Step 3: Run the lift adapter

Run the command below while passing the paths to the configuration file that contains all information required to operate this lift.

```bash
ros2 run lift_adapter_template lift_adapter_template -n LIFT_NAME -c CONFIG_FILE

#e.g.
ros2 run lift_adapter_template lift_adapter_template -n lift_1_lobby_1 -c /path/to/config.yaml
```
