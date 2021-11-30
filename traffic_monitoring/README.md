# Smart Cities Hackathon - Traffic Monitoring

To start the simulation just execute the following command:

```bash
./run-scenario.sh
```

The client for the communication between Eclipse MOSAIC and Python is included in the module `ZMessaging()` in `zmessaging.py`.

1. Import the module and create a ZMessaging object.

```python
from zmessaging import ZMessaging
server = ZMessaging()
```

2. You can receive data from Eclipse MOSAIC using the `receive_data()` method.

```python
data = server.receive_data()
>>> [b'req.interaction', b'{}']

data = server.receive_data()
>>> [b'req.interaction', b'{"veh_2":{"time":6300000000,"position":[-34.6037374383747,-58.437012648940666],"road_id":"285542308_199457966_199457934"},"veh_0":{"time":6300000000,"position":[-34.6037374383747,-58.437012648940666],"road_id":"285542308_199457966_199457934"},"veh_1":{"time":6300000000,"position":[-34.6037374383747,-58.437012648940666],"road_id":"285542308_199457966_199457934"}}']
```
Calling the method will return the latest data.
Hint: Time unit is nanoseconds [ns].

3. You can send DENM warning to Eclipse MOSAIC using the `send_warning(str)` method, where `str` is a string with the road id.

```python
server.send_warning("invalid_road_id") # Invalid road ID
>>> [b'service.warning_report', b'false']

server.send_warning("285542308_199457966_199457934") # Valid road ID
>>> [b'service.warning_report', b'true']
```

4. You can let the simulation run in the background while you develop your algorithm.