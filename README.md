# ConnectiCity

To build the Docker container:
```
docker build . -t connecticity 
```

To run the Docker container:
```
docker run -it -v $(pwd)/eclipse-mosaic-21.1:/mosaic -p 8888:8888 connecticity /bin/bash
```

Within the container run:
`jupyter lab --ip="0.0.0.0" --allow-root`


For creating the client symlinks for the Mosaic scenario run:
```
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/scenario_config.json ./scenario_config.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/cell/network.json ./cellular_network.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/sns/sns_config.json ./adhoc_network.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/mapping/mapping_config.json ./mapping_config.json
```
