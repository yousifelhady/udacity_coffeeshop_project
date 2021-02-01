# Coffee Shop Backend

## Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. 
- The backend app runs at `http://127.0.0.1:5000/`
- Authentication: Provided by Auth0 as 3rd party Authentication Service.
- SQLite database file is included under `./src/database` "database.db"


## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.
Each time you open a new terminal session, run:
```bash
set FLASK_APP=api.py;
```

To run the server, execute:
```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Error Handling

Errors are returned as JSON objects in the following format:
```bash
{
    "success": False,
    "error": 404,
    "message": "Not Found"
}
```
The API will return all the HTTPException errors types when requests fail or something goes wrong in the JSON format shown


## Endpoint Library

```
GET '/drinks'
GET '/drinks-detail'
POST '/drinks'
PATCH '/drinks/<int:drink_id>'
DELETE '/drinks/<int:drink_id>'
```


## Permissions

Barista can only perform the following action(s):
```
get:drinks-detail
```

While the Manager can perform the following action(s):
```
get:drinks-detail
post:drinks
patch:drinks
delete:drinks
```

Both of them can show all available drinks in the Drink Menu.
