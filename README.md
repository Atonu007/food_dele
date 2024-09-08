
## Restaurant Inventory and Order Management System
This project is a Django-based application designed to manage restaurant inventories and orders. It provides functionalities for handling items, modifiers, orders, employees, and restaurants through a RESTful API built with Django REST Framework (DRF).

## Features

Item Management: Add, list, update, and delete items in the restaurant's inventory.
Modifier Group Management: Create, list, update, and delete groups that categorize modifiers.
Modifier Management: Add, list, update, and delete modifiers for customizations.
Order Management:
For restaurant owners and employees: View and update orders.
For customers: Place, view, and cancel orders.
Employee Management: List and view details of employees associated with a restaurant.
Restaurant Management: View a list of all restaurants and detailed information about specific ones.


## for testing

Clone the repository:

```bash
git clone <repository-url>
cd <project-directory>
```



Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Apply database migrations:

```bash
python manage.py migrate

```

Create a superuser:

```bash
python manage.py createsuperuser


```


Run the development server:

```bash
python manage.py runserver


```
