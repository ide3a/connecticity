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
