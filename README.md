# camuzzi-wallet

Welcome to camuzzi-wallet project!

This is my solution for the Wallet challenge as specified on the Wallet.md file.

The project consists of the implementation of a simple API for a wallet application that allows an user to register his credit cards and automatically choose the best card for a transaction based on its due date and available credit.

The API was implemented in Django, a Python Web framework which makes easier to build a web app ready for production quickly.

Follow below the documentation for the implemented endpoints, instructions for testing the API on its current state and a short list of the next steps for making the app ready for production.


1. Endpoints

1.1. Authentication 

  The authentication system is Django default's with no additional customization (https://docs.djangoproject.com/en/3.0/topics/auth/default/).
  
  These are the main endpoints used for testing the API:

  http://{BASE_URL}/admin/  
    - Access the admin page.  
    - This is the default Django administration page which allows the admin user to add, change and delete content. Currently this is the only way for creating a new User using the available endpoints as explained below on the testing instructions.
	
  http://{BASE_URL}/accounts/login
  - The login page for a regular user built upon the default Django admin template.
	
  http://{BASE_URL}/accounts/logout
  - Endpoint for logging out current user.
	
1.2. Managing the Wallet

  GET http://{BASE_URL}/walletApp/getwalletinfo/
    - Retrieve a json-encoded object with basic wallet information:
      - owner: username which is the owner of the wallet.
      - max_limit: maximum limit of credit on the wallet.
      - user_limit: limit of credit self-imposed by the user, empty value meaning max_limit is being used.
      - balance: total balance of the credit cards on the wallet.
      - available_credit: available credit on the wallet considering its balance and credit limit.
		
  GET http://{BASE_URL}/walletApp/getcards/
    - Retrieve a json-encoded dictionary of key-value objects with each card information:
      - key: credit card number
      - value: credit card information:
        - dueDate: Day of the monthly payment due date.
        - validThru: Date of expiration of the credit card number.
        - name: Name as printed on card.
        - secureCode: Secure code for completing a purchase.
        - creditLimit: Limit of credit on the card.
        - balance: Current balance on the credit account.
        - available_credit: available credit on the account considering its limit and balance.
			
  POST http://{BASE_URL}/walletApp/addcard/
    - Add a new card to the user wallet with inputted values on form-data added to request body:
      - number: credit card number to be added on the wallet.
      - duedateday: day of the monthly payment due date.
      - validthruyear: year of expiration of the credit card number with 4 digits (YYYY).
      - validthrumonth: month of expiration of the credit card number with 2 digits (MM).
      - name: Name as printed on card.
      - securecode: Secure code for completing a purchase.
      - creditlimit: Limit of credit on the card.
      - balance: Current balance on the credit account.
		
  POST http://{BASE_URL}/walletApp/rmcard/
    - Removes specified card from user wallet (and from the database). Credit card number inputted on form-data added to request body:
      - number: credit card number to be removed from the wallet.

  POST http://{BASE_URL}/walletApp/addpurchase/
    - Adds a purchase to the wallet which is added to the card (or cards) according to the priorities specified on the Wallet.md file. Purchase value is inputted on form-data added to request body:
      - value: value of the purchase to be added to the wallet.
		
  POST http://{BASE_URL}/walletApp/setlimit/
    - Set the self-imposed user limit to the credit available on the wallet. Limit value is inputted on form-data added to request body:
      - userlimit: value of the limit setted by user. (empty value for using max_limit).
		
	
1.3. Managing the Card

  POST http://{BASE_URL}/walletApp/releasecredit/
    - Release credit on the card. Card number and amount to release as inputted on form-data added to request body:
      - cardnumber: credit card number
      - value: value of the amount to release.
		
		
2. Testing the API:

	- Preconditions:
    - Install Python 3

	- Clone this project into any local directory:
		$ git clone https://github.com/hdtcamuzzi/camuzzi-wallet.git
		
	- Install Python dependencies:
		$ cd camuzzi-wallet
		$ pip install -r requirements.txt
		
	- Set-up the database:
		$ cd camuzziwallet
		$ python manage.py migrate
		
	- Create a superuser account:
		$ python manage.py createsuperuser

	- Run the server application:
		$ python manage.py runserver
		
	- It should start the development server on http://127.0.0.1:8000/ 
		
	- Access the admin page on any browser for creating the first user:
		- Access http://127.0.0.1:8000/admin/
		- Login with the admin account just created.
		- Under "Authentication and Authorization", click on "Users and on "Add User +" 
		- Enter the new user credentials and click on "Save"
		- Log out the admin user: http://127.0.0.1:8000/accounts/logout
		
	- You can starting using the API with the newly created user.
	
	- The json file "CamuzziWallet_API_test.postman_collection.json" can be imported on Postman (https://www.postman.com/downloads/)
	
	- It will open a collection with the endpoints already configured to test the API.
	
	- Please not it is necessary to manually input the CSRF token and sessionid cookie on Postman in order to validate the API with Django authentication system:
	
  - Login the user by sending a POST request to the login page including the user credentials as form-data:
		
	  POST http://127.0.0.1:8000/accounts/login
		  Body (form-data):
			  username = user
				password = pass
					
	- You should receive a "403" response (Forbidden), however it is possible to get the CSRF token from the request Cookies as Django is on Debug mode.
				
	- Copy the token and add to the request Headers with key "X-CSRFToken", then it should be possible to re-send the Login request and get the sessionid Cookie which identify the user.
			
  - Copy the sessionid parameter obtained from the Cookies.
		
	- You must insert both Headers on every other request you perform with postman, so the user will be authenticated during the requests. (Please note the CSRF token may expire, you can obtain a new one inspecting the received cookies).
		
			Cookie: sessionid={session_id}
			X-CSRFToken: {csrf_token}
			
	- With this, all endpoints documented above will work according to the authenticated user.
			
		
					









