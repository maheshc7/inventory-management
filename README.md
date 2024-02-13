# Kaizntree - Inventory Management - Backend Task

## Introduction
Django REST Framework serving data to front-end dashboards similar to the Kaizntree's item dashboard.
[Hosted on AWS.](http://34.208.86.103:8000/)


## Requirements
```bash
Django==5.0.2
djoser==2.2.2
djangorestframework==3.14.0
drf-yasg==1.21.7
```

## Getting Started


1. **Clone the repository:**
    ```bash
    git clone git@github.com:maheshc7/inventory-management.git
    cd inventory_management
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run Migrations:**
    ```bash
    python manage.py migrate
    ```

4. **Create a Superuser:**
    ```bash
    python manage.py createsuperuser
    ```

5. **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```

6. **Access the API:**
    Open your browser and go to [http://localhost:8000/](http://localhost:8000/)

## API Documentation
Provide a link to your API documentation or instructions on how to access it.
Go to [Swagger Doc](http://34.208.86.103:8000/swagger/) or [ReDoc](http://34.208.86.103:8000/redoc/) to view the API Docs.

## API Endpoints


- **Endpoint 1:** `/api/item/?category=Raw Materials`
    - Description: Returns list of items available in the database. Can be filtered and paginated via query parameters.
    - Method: GET
    - Parameters: List any required parameters.

- **Endpoint 2:** `/api/item`
    - Description: Add/Create new item.
    - Method: POST
    - Parameters: See swagger doc.

...

## Frontend Task:
[Link to CodeBox](https://codesandbox.io/s/k89fsd)


