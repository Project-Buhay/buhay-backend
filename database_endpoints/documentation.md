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

Given a list of `Point`s of longitude-latitude coordinates, this endpoint returns the `location_names: list[str]` that represents the street address of each coordinate, in the same order.

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
    "location_names": [
        "University of the Philippines Alumni Engineers' Centennial Hall, P. Velasquez Street, Diliman, Quezon City, 1800 Metro Manila, Philippines",
        "41-B Mapagkawanggawa, Diliman, Lungsod Quezon, 1101 Kalakhang Maynila, Philippines"
    ]
}
```

