# Experimental environment introduction

Just `docker compose up` to get the service up.

This service is a product microservice that handles CRUD for a single product and saves the results in a database. For ease of use, I'm using Redis as the database for this example.

This service has two entry points.
1. http://localhost:50000 is the home page of the microservice, with a simple list page and blocks for adding and modifying products.
2. http://localhost:50000/apidocs is the swagger home page, which lists all the API descriptions and specifications.

Then prepare some basic test data.

```bash
curl -X POST "http://localhost:50000/api/product" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "id=123&name=Apple&description=Fruit"
curl -X POST "http://localhost:50000/api/product" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "id=234&name=Bird&description=Animal"
curl -X POST "http://localhost:50000/api/product" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "id=345&name=Cat&description=Animal"
```

The full examples are actually listed in [rest_api_calling.ipynb](https://github.com/wirelessr/genai_api_calling/blob/main/rest_api_calling.ipynb).
