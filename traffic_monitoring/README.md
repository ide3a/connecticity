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
>>>[b'req.interaction', b'{"time":11000000000,"array":[{"position":[-34.62937414680087,-58.41312814826621],"roadId":"334573426_206105939_194118109"},{"position":[-34.60815103123608,-58.45093127124559],"roadId":"221689286_193839793_193839792"},{"position":[-34.597858263034176,-58.41397855347756],"roadId":"71179546_81832377_81614080"},{"position":[-34.60327635551888,-58.41154155816103],"roadId":"48397526_192899622_196138117"},{"position":[-34.61727210402623,-58.44443484237213],"roadId":"221688948_206134688_206134686"},{"position":[-34.61499386056854,-58.43223641977625],"roadId":"129788154_206133028_206133029"},{"position":[-34.61929005005386,-58.42717587869354],"roadId":"48743381_206133139_206133134"}]}']
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