# ConnectiCity

To run the Docker container based on the image from Docker hub:
```
docker compose up
```

To open the jupyter hub in your brower go to:
```
localhost:8888/lab?token=smart_city_hackathon
```

For creating the client symlinks for the Mosaic scenario run:
```
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/scenario_config.json ./scenario_config.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/cell/network.json ./cellular_network.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/sns/sns_config.json ./adhoc_network.json
ln -s ../eclipse-mosaic-21.1/scenarios/Barnim/mapping/mapping_config.json ./mapping_config.json
```
