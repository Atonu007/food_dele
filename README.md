# Food Delivery Management System API Documentation

### Project Overview
This API provides functionalities for a food delivery management system, enabling restaurant owners, employees, and customers to manage restaurant inventories, orders, and user roles efficiently. It supports features such as user authentication, order processing, inventory management, and payment transactions.

### Technical Requirements
Python: 3.8 or higher

Django: 5.1.1

Django REST Framework (DRF): 3.15.2

Dependencies: Install required packages with:

```bash
pip install -r requirements.txt

```


## API Endpoints
1. Authentication
   
Register Users

Endpoint: /user/register/

Method: POST

Purpose: Registers a new user (restaurant owner, employee, or customer).


User Login

Endpoint: /user/login/

Method: POST

Purpose: Authenticates users and returns a token for subsequent requests.

2. Orders
   
List of All Orders for Owner and Employee

Endpoint: /order/restaurant-orders/

Method: GET

Purpose: Retrieves a list of all orders associated with the restaurant of the authenticated user.

Update or Cancel Order

Endpoint: /order/orders/<order_id>/update-status/

Method: PATCH

Purpose: Updates the status of a specific order. Users must have the role of either owner or employee.


3. Employee Operations
   
List of All Employees

Endpoint: /user/employees/

Method: GET

Purpose: Retrieves a list of employees associated with the authenticated restaurant owner.

Detail Employee

Endpoint: /user/employees/<employee_id>/

Method: GET

Purpose: Retrieves detailed information about a specific employee by their ID.

4. Customer Operations
   
Create Order

Endpoint: /order/create/

Method: POST

Purpose: Allows authenticated customers to create a new order.

List of Orders

Endpoint: /order/orders/

Method: GET

Purpose: Retrieves a list of all orders associated with the authenticated customer.

Cancel Order

Endpoint: /order/orders/<order_id>/cancel/

Method: POST

Purpose: Allows customers to cancel an existing order if it is in the "pending" state.

5. Restaurant Operations
   
List of All Restaurants

Endpoint: /user/restaurants/

Method: GET

Purpose: Retrieves a paginated list of all restaurants accessible to authenticated customers.

Detail Restaurant

Endpoint: /user/restaurants/<restaurant_id>/

Method: GET

Purpose: Retrieves detailed information about a specific restaurant by its ID.

6. Category Management
   
Create Category

Endpoint: /inventory/categories/

Method: POST

Purpose: Creates a new category within the restaurant's inventory.

List Categories

Endpoint: /inventory/categories/

Method: GET

Purpose: Retrieves a list of all categories associated with the authenticated restaurant.

Update Category

Endpoint: /inventory/categories/<category_id>/

Method: PATCH

Purpose: Updates an existing category.

Delete Category

Endpoint: /inventory/categories/<category_id>/

Method: DELETE

Purpose: Deletes a specific category from the inventory.

7. Modifier Group Management
   
Create Modifier Group

Endpoint: /inventory/modifier-groups/

Method: POST

Purpose: Creates a new modifier group for menu items.

List Modifier Groups

Endpoint: /inventory/modifier-groups/

Method: GET

Purpose: Retrieves a list of all modifier groups.

Update Modifier Group

Endpoint: /inventory/modifier-groups/<modifier_group_id>/

Method: PATCH

Purpose: Updates an existing modifier group.

Delete Modifier Group

Endpoint: /inventory/modifier-groups/<modifier_group_id>/

Method: DELETE

Purpose: Deletes a specific modifier group.

8. Modifier Management
   
Create Modifier

Endpoint: /inventory/modifiers/

Method: POST

Purpose: Creates a new modifier within a modifier group.

List Modifiers

Endpoint: /inventory/modifiers/

Method: GET

Purpose: Retrieves a list of all modifiers.

Update Modifier

Endpoint: /inventory/modifiers/<modifier_id>/

Method: PATCH

Purpose: Updates an existing modifier.

Delete Modifier

Endpoint: /inventory/modifiers/<modifier_id>/

Method: DELETE

Purpose: Deletes a specific modifier.



## Error Handling

The API will return standard HTTP status codes for different scenarios:

200 OK: Successful request

400 Bad Request: Invalid data

401 Unauthorized: Authentication failure

403 Forbidden: Permission denied

404 Not Found: Resource not found

500 Internal Server Error: Server error

## Authentication

To access protected endpoints, include the Authorization header with the token received upon successful login:

```bash
Authorization: Token <your_token_here>

```


## Setup Instructions

Clone the repository:

```bash
git clone <repository_url>
cd <repository_directory>

```
Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

Install dependencies:

```bash
pip install -r requirements.txt

```
Apply migrations:

```bash
python manage.py migrate

```
Run the development server:

```bash
python manage.py runserver

```


## Conclusion

This API documentation provides a comprehensive overview of the Food Delivery Management System API, including its functionalities and endpoints. For further details or assistance, please feel free to reach out.




