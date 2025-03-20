# TSP Endpoint

The _tsp endpoint_ accepts a GET Request at the `/tsp` path. This request contains a list of <b>n</b> `Point`s which follows the format below.
```python
[
    {
        "location_name" : str|None,
        "coordinates" : [lat: float, lng: float]
    }
]
```

The endpoint then returns a list of <b>n</b> `Point`s such that:
<br /> - The sequence of `Point`s is the shortest path that visits all of the given points from the input. 
<br /> - The weight of each edge from one point to another is the haversine distance between the two points.
<br /> - The returned path always starts with the _0th_ point from the input list.

### Dependencies 

The _tsp endpoint_ uses [FastAPI] for its implementation to receive GET Requests.

It uses the `Graph` data structure and `travelling_salesman_problem()` function from [NetworkX] to solve for the shortest path. Additionally, the `great_circle()` function from [OSMnx] was used to calculate the haversine distance between each point pair.

[FastAPI]: https://fastapi.tiangolo.com
[NetworkX]: https://networkx.org/documentation/stable/index.html
[OSMnx]: https://osmnx.readthedocs.io/en/stable/index.html

### Input Schema
The _tsp endpoint_'s input is validated using [Pydantic] with the schema below. By using Pydantic, the _tsp endpoint_ raises an `HTTP Exception` with the `422_Unprocessable_Entity` status code. 

[Pydantic]: docs.pydantic.dev
``` python
from pydantic import BaseModel

class Point(BaseModel):
    location_name: str | None
    coordinates: Tuple[float, float] #[lat: float, lng: float]
```

### Auxiliary Functions

#### create_graph
Takes in a list of `Point`s and then returns a complete, weighted, undirected graph of type `networkx.Graph` such that the weight of edge <b>(i, j)</b> is the haversine distance between points <b>i</b> and <b>j</b>.

#### append_starting_node
Takes in a graph <b>G</b> of type `networkX.Graph` and a list of `Point`s <b>tsp_route</b> that act as the shortest Hamiltonian path containing points 1 through n-1 (remember, we are using 0-indexing).
The 0th node of <b>G</b> is then appended to either the left or the right end of <b>tsp_route</b>, depending on which is closer with respect to their haversine distances.
Should the 0th node be appended to the right side of <tsp_route>, the resulting list would be reversed so that the output would start with the 0th node of <b>G</b>.

#### node_to_json_parser
Takes in a list of `Points`, which are in a Python format, and then converts them into JSON so that they could be read as the output of _tsp endpoint_.
