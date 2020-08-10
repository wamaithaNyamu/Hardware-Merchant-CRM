

![Landing page](./landing.PNG)

![about page](./about.PNG)
# Description of the System: 


This is a system that stores credit card information for customers by the merchant in a secure vault. This information is collected only once and next time a customer is invoiced, the merchant can use the stored card information. The information is encrypted and hashed using SHA and there are different user levels for example, super administration of the system, the administrator and user. All these are authenticated and can only access the data according to their level of privilege. 

# Registration page

A new user wishing to purchase a product from the website must first have an account. 

![registration page](./register.PNG)

# Login Page
   
This is a view of the login page in case the user comes back to purchase something. 

![login page](./login.PNG)

# User view

By default all new signups are assigned a class of Customer

![user page](./customer.PNG)

The customer can edit their credit card info. Only the customer can view their credit card info.
The cvv and credit card info is encrypted using AES in the db thus even of the db was hacked the
hackers would not know the credit card details. Furthermore even the super user views encrypted credit card details and cvv in the django admin.
The supervisor can send invoices but the credit card details are only visible in the email.

![cards page](./cards.PNG)
![aes page](./aes.PNG)
![email page](./email.PNG)

# Supervisor views

![supervisor page](./supervisor.PNG)
![invoice page](./invoice.PNG)

# Superuser view

![superuser page](./superuser.PNG)

# Database Schema

![schema](./schema.jpeg)

# Normalised database to 3NF

![normdb](./normdb.PNG)