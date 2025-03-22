This file serves as documentation for all database endpoints.

- [/login](#login)
- [/convert_coordinates](#convert_coordinates)

# /login

Given a `username: str` and a `password: str`, this endpoint will check if a person in the `people` table of the database exists such that their username and password match the given.

If there is a match, the endpoint will return the `person_id: int` and `access_control: int` of that person.

**Sample Input of Valid Login Credentials**
```JSON
{
    "username": "Constituent1",
    "password": "Constituent1"
}
```
**Sample Output of Valid Login Credentials**
```JSON
{
    "person_id": 1,
    "access_control": 1
}
```

If there is no match, the endpoint will return `person_id = 0` and `access_control = 0` since this case would be impossible normally. 

**Sample Input of Invalid Login Credentials**
```JSON
{
    "username": "UserNameThatIsNotInDatabase",
    "password": "PasswordThatIsNotInDatabase"
}
```

**Sample Output of Invalid Login Credentials**
```JSON
{
    "person_id": 0,
    "access_control": 0
}
```

# /convert_coordinates

Given a list of `Point`s of longitude-latitude coordinates, this endpoint returns the `locations: list[str]` that represents the street address of each coordinate, in the same order.

**Sample Input**
```JSON
[
    {
        "coordinates": [
            121.06846773745589,
            14.648772127025484
      ]
    },
    {
        "coordinates":[
            121.05786349512705,
            14.643245228663027
        ]
    }
]
```

**Sample Output**
```JSON
{
    "locations": [
        "University of the Philippines Alumni Engineers' Centennial Hall, P. Velasquez Street, Diliman, Quezon City, 1800 Metro Manila, Philippines",
        "41-B Mapagkawanggawa, Diliman, Lungsod Quezon, 1101 Kalakhang Maynila, Philippines"
    ]
}
```

# /add_request

Given a `person_id: int` and `coordinates: List[Point]`, the endpoint inserts a new row into the `dispatcher_data` table with the fields below and then returns the `request_id` of the inserted row: 

```JSON
{
    "request_id": int, // (new incremented primary key),
    "coordinate_names": list[str], // (reverse geocoded coordinates)
    "consituent_id": person_id,
    "route_info_id": null,
    "rescued": false,
    "rescuer_id": null,
    "old_rescuer_id": null,
    "raw_coordinates": coordinates,
    "ongoing": false
}
```

**Sample Input**
```JSON
{
    "person_id": 3,
    "coordinates": [
        {"coordinates": ["121.0694063","14.65679956"]},
        {"coordinates": ["121.0411614","14.66310851"]},
        {"coordinates": ["121.0219046","14.65919254"]},
        {"coordinates": ["121.0177288","14.65537632"]}
    ]
}
```

**Sample Output**

*Note that the returned `request_id` is the incremented primary key of the new row.*
```JSON
{
    "request_id": 12
}
```

**Sample Inserted Row**
```JSON
{
    "request_id": 12,
    "coordinate_names": {
        "location_names": [
            "Chemical Engineering Laboratory, Magsaysay Ave, Diliman, Quezon City, 1101 Metro Manila, Philippines",
            "145 Rd 2, Quezon City, 1100 Metro Manila, Philippines",
            "M25C+MQJ, 20 Ilocos Sur, Bago Bantay, Lungsod Quezon, 1105 Kalakhang Maynila, Philippines",
            "301 San Antonio, Quezon City, Metro Manila, Philippines"
        ]
    },
    "constituent_id": 3,
    "route_info_id": null,
    "rescued": false,
    "rescuer_id": null,
    "old_rescuer_id": null,
    "raw_coordinates": {
        "raw_coordinates": [
            {"coordinates": [121.0694063, 14.65679956]},
            {"coordinates": [121.0411614, 14.66310851]},
            {"coordinates": [121.0219046, 14.65919254]},
            {"coordinates": [121.0177288, 14.65537632]}
        ]
    },
    "ongoing": false
}
```

# /save_route

The endpoint is given a request ID `request_id: int`, a starting point `start: Point` and some other points `other_points: List[Point]`. A new row that contains the TSP solution for the given points with their safe routes/directions from going point to point is inserted into the `route_info` table with its unique `route_id`. Then, the new `route_id` becomes the `route_info_id` of the row in `dispatcher_data` with `request_id` as its primary key.  

**Sample Input**
```JSON
{
  "start": {
    "coordinates": ["121.0694063","14.65679956"]
  },
  "other_points": [
    {"coordinates": ["121.0411614", "14.66310851"]},
    {"coordinates": ["121.0219046", "14.65919254"]},
    {"coordinates": ["121.0177288","14.65537632"]}
  ]
}
```

**Sample Output**
```JSON
{"success": true}
```

**Sample Inserted Row in Route_Info**

*Note: `route_id` is the incremented primary id of the new row. 
```JSON
    "route_id": 6,
    "route_data": {
        "routes": [
            {
                "start": "Chemical Engineering Laboratory, Magsaysay Ave, Diliman, Quezon City, 1101 Metro Manila, Philippines",
                "end": "145 Rd 2, Quezon City, 1100 Metro Manila, Philippines",
                "data": {
                    // Very long data
                }
            },
            {
                "start": "145 Rd 2, Quezon City, 1100 Metro Manila, Philippines",
                "end": "M25C+MQJ, 20 Ilocos Sur, Bago Bantay, Lungsod Quezon, 1105 Kalakhang Maynila, Philippines",
                "data": {
                    // Very long data
                }
            },
            {
                "start": "M25C+MQJ, 20 Ilocos Sur, Bago Bantay, Lungsod Quezon, 1105 Kalakhang Maynila, Philippines",
                "end": "301 San Antonio, Quezon City, Metro Manila, Philippines",
                "data": {
                    // Very long data
                }
            },
            {
                "start": "301 San Antonio, Quezon City, Metro Manila, Philippines",
                "end": "Chemical Engineering Laboratory, Magsaysay Ave, Diliman, Quezon City, 1101 Metro Manila, Philippines",
                "data": {
                    // Very long data
                }
            }
        ]
    }
```

**Sample Updated Row in dispatcher_data**
```JSON
{
    "request_id": 12,
    // Other Fields remain the same
    "route_info_id": 6
    // Other Fields remain the same
}
```