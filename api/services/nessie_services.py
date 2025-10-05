# This service class handles ALL communication with Capital One's Nessie API.

# Standard Python imports
import httpx    
import os                                    
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NessieService:
   """
   Service class for interacting with Capital One Nessie API
  
   This class handles:
   - API authentication (API key management)
   - HTTP request/response handling
   - Error handling and logging
   - Data fetching from various Nessie endpoints
   - URL construction and parameter handling
   """
  
   def __init__(self):
       """
       Initialize the Nessie service with configuration from environment variables
      
       Environment Variables Required:
       - NESSIE_API_KEY: Your Nessie API key from nessieisreal.com
       - NESSIE_BASE_URL: Base URL for Nessie API (optional, defaults to official URL)
       """
       # Get the base URL for Nessie API from environment or use default
       self.base_url = os.getenv("NESSIE_BASE_URL", "http://api.nessieisreal.com")
      
       # Get the API key from environment variables
       # This is REQUIRED - you must sign up at nessieisreal.com to get one
       self.api_key = os.getenv("NESSIE_API_KEY")
      
       # Warn if API key is missing - the service won't work without it
       if not self.api_key:
           logger.warning("NESSIE_API_KEY not found in environment variables")
      
       # Set timeout for HTTP requests (30 seconds)
       # This prevents hanging requests if Nessie API is slow
       self.timeout = 30.0
  
   def _build_url(self, endpoint: str) -> str:
       """
       Build complete URL with API key for Nessie API requests
      
       How Nessie API authentication works:
       - Nessie uses API key authentication via URL parameter
       - Every request must include ?key=YOUR_API_KEY or &key=YOUR_API_KEY
       - This method automatically adds the key to any endpoint
      
       Args:
           endpoint (str): The API endpoint path (e.g., "/customers" or "/accounts")
      
       Returns:
           str: Complete URL with API key (e.g., "http://api.nessieisreal.com/customers?key=abc123")
      
       Examples:
           _build_url("/customers") -> "http://api.nessieisreal.com/customers?key=YOUR_KEY"
           _build_url("/accounts?type=checking") -> "http://api.nessieisreal.com/accounts?type=checking&key=YOUR_KEY"
       """
       # Determine if we need ? or & based on whether endpoint already has parameters
       separator = "&" if "?" in endpoint else "?"
      
       # Combine base URL + endpoint + separator + API key
       return f"{self.base_url}{endpoint}{separator}key={self.api_key}"
  
   async def _make_request(self, endpoint: str, method: str = "GET", data: Optional[Dict] = None) -> Dict[str, Any]:
       """
       Make HTTP request to Nessie API with comprehensive error handling
      
       This is the core method that handles ALL HTTP communication with Nessie.
       It's async to avoid blocking the web server while waiting for API responses.
      
       Args:
           endpoint (str): API endpoint to call (e.g., "/customers", "/accounts")
           method (str): HTTP method - GET, POST, PUT, DELETE (default: GET)
           data (Optional[Dict]): JSON data to send in request body (for POST/PUT)
      
       Returns:
           Dict[str, Any]: JSON response from Nessie API parsed into Python dict
      
       Raises:
           Exception: With descriptive error message if request fails
          
       Error Handling:
       - Timeout errors: If Nessie API is slow or unresponsive
       - HTTP errors: If Nessie returns 4xx or 5xx status codes
       - Network errors: If can't connect to Nessie at all
       - JSON errors: If Nessie returns invalid JSON
       """
       # Build the complete URL with API key
       url = self._build_url(endpoint)
       print(f"Making {method} request to Nessie API: {url}")
       try:
           # Create async HTTP client with timeout
           async with httpx.AsyncClient(timeout=self.timeout) as client:
              
               if method == "GET":
                   response = await client.get(url)
               elif method == "POST":
                   response = await client.post(url, json=data)
               elif method == "PUT":
                   response = await client.put(url, json=data)
               elif method == "DELETE":
                   response = await client.delete(url)
               else:
                   raise ValueError(f"Unsupported HTTP method: {method}")
              
               response.raise_for_status()
               return response.json()
              
       except httpx.TimeoutException:
           raise Exception(f"Request to Nessie API timed out: {endpoint}")
          
       except httpx.HTTPStatusError as e:
           raise Exception(f"Nessie API error {e.response.status_code}: {e.response.text}")
          
       except Exception as e:
           raise Exception(f"Failed to connect to Nessie API: {str(e)}")
  
   async def get_customers(self) -> List[Dict[str, Any]]:
       """
       Fetch all customers from Nessie API
      
       Returns a list of all customer records in the Nessie system.
       Each customer represents a person who can have bank accounts.
      
       Returns:
           List[Dict[str, Any]]: List of customer objects
          
       Customer Object Structure:
       {
           "_id": "507f1f77bcf86cd799439011",     # Unique customer ID
           "first_name": "John",                 # Customer's first name
           "last_name": "Doe",                   # Customer's last name
           "address": {                          # Customer's address
               "street_number": "123",
               "street_name": "Main St",
               "city": "Anytown",
               "state": "NY",
               "zip": "12345"
           }
       }
      
       Raises:
           Exception: If API call fails or returns error
       """
       try:
           # Make GET request to /customers endpoint
           return await self._make_request("/customers")
       except Exception as e:
           logger.error(f"Failed to fetch customers: {e}")
           raise Exception(f"Failed to fetch customers: {str(e)}")
  
   async def get_customer(self, customer_id: str) -> Dict[str, Any]:
       """
       Fetch a specific customer by their ID
      
       Args:
           customer_id (str): The unique customer identifier from Nessie
          
       Returns:
           Dict[str, Any]: Single customer object with full details
          
       Raises:
           Exception: If customer not found or API call fails
          
       Example:
           customer = await service.get_customer("507f1f77bcf86cd799439011")
       """
       try:
           # Make GET request to /customers/{customer_id} endpoint
           return await self._make_request(f"/customers/{customer_id}")
       except Exception as e:
           logger.error(f"Failed to fetch customer {customer_id}: {e}")
           raise Exception(f"Failed to fetch customer {customer_id}: {str(e)}")
  
   async def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Create a new customer
      
       Args:
           customer_data (Dict[str, Any]): Customer data to create
          
       Customer Data Structure:
       {
           "first_name": "John",                 # Customer's first name (required)
           "last_name": "Doe",                   # Customer's last name (required)
           "address": {                          # Customer's address (required)
               "street_number": "123",
               "street_name": "Main St",
               "city": "Anytown",
               "state": "NY",
               "zip": "12345"
           }
       }
      
       Returns:
           Dict[str, Any]: Created customer object with assigned ID
          
       Example:
           new_customer = {
               "first_name": "John",
               "last_name": "Doe",
               "address": {
                   "street_number": "123",
                   "street_name": "Main St",
                   "city": "Anytown",
                   "state": "NY",
                   "zip": "12345"
               }
           }
           result = await service.create_customer(new_customer)
       """
       try:
           # Make POST request to /customers endpoint with data
           return await self._make_request("/customers", method="POST", data=customer_data)
       except Exception as e:
           logger.error(f"Failed to create customer: {e}")
           raise Exception(f"Failed to create customer: {str(e)}")
  
   async def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Update a specific customer by their ID
      
       Args:
           customer_id (str): The unique customer identifier
           customer_data (Dict[str, Any]): Customer data to update
          
       Returns:
           Dict[str, Any]: Updated customer object
          
       Example:
           updated_data = {"address": {"street_number": "456", "street_name": "Oak Ave", "city": "Newtown", "state": "CA", "zip": "54321"}}
           result = await service.update_customer("507f1f77bcf86cd799439011", updated_data)
       """
       try:
           # Make PUT request to /customers/{customer_id} endpoint
           return await self._make_request(f"/customers/{customer_id}", method="PUT", data=customer_data)
       except Exception as e:
           logger.error(f"Failed to update customer {customer_id}: {e}")
           raise Exception(f"Failed to update customer {customer_id}: {str(e)}")
  
   async def get_accounts_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
       """
       Fetch all accounts belonging to a specific customer
      
       Args:
           customer_id (str): The customer's unique identifier
          
       Returns:
           List[Dict[str, Any]]: List of account objects for this customer
          
       Account Object Structure:
       {
           "_id": "507f1f77bcf86cd799439012",       # Unique account ID
           "type": "Credit Card",                  # Account type (Credit Card, Checking, Savings)
           "nickname": "My Credit Card",           # User-friendly name
           "rewards": 10234,                       # Rewards points balance
           "balance": 1203.42,                     # Current account balance
           "account_number": "123456789",          # Account number
           "customer_id": "507f1f77bcf86cd799439011"  # ID of owning customer
       }
      
       Example:
           accounts = await service.get_accounts_by_customer("507f1f77bcf86cd799439011")
       """
       try:
           # Make GET request to /customers/{customer_id}/accounts endpoint
           return await self._make_request(f"/customers/{customer_id}/accounts")
       except Exception as e:
           logger.error(f"Failed to fetch accounts for customer {customer_id}: {e}")
           raise Exception(f"Failed to fetch accounts for customer {customer_id}: {str(e)}")
  
   async def get_all_accounts(self) -> List[Dict[str, Any]]:
       """
       Fetch all accounts in the system regardless of customer
      
       Returns:
           List[Dict[str, Any]]: List of all account objects
          
       Note:
           This returns accounts for ALL customers. Use get_accounts_by_customer()
           if you want accounts for a specific customer only.
       """
       try:
           # Make GET request to /accounts endpoint
           return await self._make_request("/accounts")
       except Exception as e:
           logger.error(f"Failed to fetch all accounts: {e}")
           raise Exception(f"Failed to fetch all accounts: {str(e)}")
  
   async def get_account(self, account_id: str) -> Dict[str, Any]:
       """
       Fetch a specific account by its ID
      
       Args:
           account_id (str): The unique account identifier
          
       Returns:
           Dict[str, Any]: Single account object with full details
          
       Example:
           account = await service.get_account("507f1f77bcf86cd799439012")
       """
       try:
           # Make GET request to /accounts/{account_id} endpoint
           return await self._make_request(f"/accounts/{account_id}")
       except Exception as e:
           logger.error(f"Failed to fetch account {account_id}: {e}")
           raise Exception(f"Failed to fetch account {account_id}: {str(e)}")
  
   async def create_account(self, customer_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Create a new account for a specific customer
      
       Args:
           customer_id (str): The customer's unique identifier
           account_data (Dict[str, Any]): Account data to create
          
       Account Data Structure:
       {
           "type": "Checking",                   # Account type: "Checking", "Savings", or "Credit Card" (required)
           "nickname": "My Checking Account",    # User-friendly name (required)
           "rewards": 0,                         # Initial rewards points (required)
           "balance": 1000,                      # Initial balance (required)
           "account_number": "1234567890123456"  # 16-digit account number (optional)
       }
      
       Returns:
           Dict[str, Any]: Created account object with assigned ID
          
       Example:
           new_account = {
               "type": "Checking",
               "nickname": "My Checking Account",
               "rewards": 0,
               "balance": 1000
           }
           result = await service.create_account("507f1f77bcf86cd799439011", new_account)
       """
       try:
           # Make POST request to /customers/{customer_id}/accounts endpoint with data
           return await self._make_request(f"/customers/{customer_id}/accounts", method="POST", data=account_data)
       except Exception as e:
           logger.error(f"Failed to create account for customer {customer_id}: {e}")
           raise Exception(f"Failed to create account for customer {customer_id}: {str(e)}")
  
   async def update_account(self, account_id: str, account_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Update a specific account by its ID
      
       Args:
           account_id (str): The unique account identifier
           account_data (Dict[str, Any]): Account data to update
          
       Returns:
           Dict[str, Any]: Updated account object
          
       Example:
           updated_data = {"nickname": "Updated Account Name", "account_number": "9876543210987654"}
           result = await service.update_account("507f1f77bcf86cd799439012", updated_data)
       """
       try:
           # Make PUT request to /accounts/{account_id} endpoint
           return await self._make_request(f"/accounts/{account_id}", method="PUT", data=account_data)
       except Exception as e:
           logger.error(f"Failed to update account {account_id}: {e}")
           raise Exception(f"Failed to update account {account_id}: {str(e)}")
  
   async def delete_account(self, account_id: str) -> Dict[str, Any]:
       """
       Delete a specific account by its ID
      
       Args:
           account_id (str): The unique account identifier
          
       Returns:
           Dict[str, Any]: Deletion confirmation response
          
       Example:
           result = await service.delete_account("507f1f77bcf86cd799439012")
       """
       try:
           # Make DELETE request to /accounts/{account_id} endpoint
           return await self._make_request(f"/accounts/{account_id}", method="DELETE")
       except Exception as e:
           logger.error(f"Failed to delete account {account_id}: {e}")
           raise Exception(f"Failed to delete account {account_id}: {str(e)}")
  
   async def get_transactions_by_account(self, account_id: str) -> List[Dict[str, Any]]:
       """
       Fetch all transactions (purchases) for a specific account
      
       Args:
           account_id (str): The account's unique identifier
          
       Returns:
           List[Dict[str, Any]]: List of transaction objects for this account
          
       Transaction Object Structure:
       {
           "_id": "507f1f77bcf86cd799439013",       # Unique transaction ID
           "account_id": "507f1f77bcf86cd799439012", # Account this transaction belongs to
           "merchant_id": "507f1f77bcf86cd799439014", # Merchant where purchase was made
           "amount": 23.45,                        # Amount spent (always positive)
           "description": "Purchase at Starbucks", # Description of the transaction
           "purchase_date": "2023-10-04",         # Date of the transaction
           "medium": "balance",                    # Payment method (balance, credit_card, etc.)
           "status": "pending"                     # Transaction status
       }
      
       Example:
           transactions = await service.get_transactions_by_account("507f1f77bcf86cd799439012")
       """
       try:
           # Make GET request to /accounts/{account_id}/purchases endpoint
           return await self._make_request(f"/accounts/{account_id}/purchases")
       except Exception as e:
           logger.error(f"Failed to fetch transactions for account {account_id}: {e}")
           raise Exception(f"Failed to fetch transactions for account {account_id}: {str(e)}")
  
   async def get_all_purchases(self) -> List[Dict[str, Any]]:
       """
       Fetch all transactions (purchases) in the system regardless of account
      
       Since Nessie API doesn't have a global /purchases endpoint, this method:
       1. First fetches all accounts
       2. Then fetches purchases for each account
       3. Combines all purchases into a single list
      
       Returns:
           List[Dict[str, Any]]: List of all transaction objects from all accounts
          
       Note:
           This returns transactions for ALL accounts. Use get_transactions_by_account()
           if you want transactions for a specific account only.
       """
       try:
           logger.info("Fetching all purchases by getting purchases from each account...")
          
           # Step 1: Get all accounts first
           accounts = await self.get_all_accounts()
           logger.info(f"Found {len(accounts)} accounts, fetching purchases for each...")
          
           # Step 2: Fetch purchases for each account
           all_purchases = []
           for account in accounts:
               account_id = account.get("_id")
               if account_id:
                   try:
                       # Get purchases for this specific account
                       account_purchases = await self.get_transactions_by_account(account_id)
                       all_purchases.extend(account_purchases)
                       logger.info(f"Account {account_id}: {len(account_purchases)} purchases")
                   except Exception as e:
                       logger.warning(f"Could not fetch purchases for account {account_id}: {e}")
                       continue

           logger.info(f"Total purchases collected: {len(all_purchases)}")
           return all_purchases
          
       except Exception as e:
           logger.error(f"Failed to fetch all purchases: {e}")
           raise Exception(f"Failed to fetch all purchases: {str(e)}")
  
   async def get_purchase(self, purchase_id: str) -> Dict[str, Any]:
       """
       Fetch a specific purchase by its ID
      
       Args:
           purchase_id (str): The unique purchase identifier
          
       Returns:
           Dict[str, Any]: Single purchase object with full details
          
       Example:
           purchase = await service.get_purchase("507f1f77bcf86cd799439013")
       """
       try:
           # Make GET request to /purchases/{purchase_id} endpoint
           return await self._make_request(f"/purchases/{purchase_id}")
       except Exception as e:
           logger.error(f"Failed to fetch purchase {purchase_id}: {e}")
           raise Exception(f"Failed to fetch purchase {purchase_id}: {str(e)}")
  
   async def update_purchase(self, purchase_id: str, purchase_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Update a specific purchase by its ID
      
       Args:
           purchase_id (str): The unique purchase identifier
           purchase_data (Dict[str, Any]): Purchase data to update
          
       Returns:
           Dict[str, Any]: Updated purchase object
          
       Example:
           updated_data = {"amount": 25.99, "description": "Updated description"}
           result = await service.update_purchase("507f1f77bcf86cd799439013", updated_data)
       """
       try:
           # Make PUT request to /purchases/{purchase_id} endpoint
           return await self._make_request(f"/purchases/{purchase_id}", method="PUT", data=purchase_data)
       except Exception as e:
           logger.error(f"Failed to update purchase {purchase_id}: {e}")
           raise Exception(f"Failed to update purchase {purchase_id}: {str(e)}")
  
   async def delete_purchase(self, purchase_id: str) -> Dict[str, Any]:
       """
       Delete a specific purchase by its ID
      
       Args:
           purchase_id (str): The unique purchase identifier
          
       Returns:
           Dict[str, Any]: Deletion confirmation response
          
       Example:
           result = await service.delete_purchase("507f1f77bcf86cd799439013")
       """
       try:
           # Make DELETE request to /purchases/{purchase_id} endpoint
           return await self._make_request(f"/purchases/{purchase_id}", method="DELETE")
       except Exception as e:
           logger.error(f"Failed to delete purchase {purchase_id}: {e}")
           raise Exception(f"Failed to delete purchase {purchase_id}: {str(e)}")
  
   async def get_purchases_by_merchant(self, merchant_id: str) -> List[Dict[str, Any]]:
       """
       Fetch all purchases for a specific merchant
      
       Args:
           merchant_id (str): The merchant's unique identifier
          
       Returns:
           List[Dict[str, Any]]: List of purchase objects for this merchant
          
       Example:
           purchases = await service.get_purchases_by_merchant("507f1f77bcf86cd799439014")
       """
       try:
           # Make GET request to /merchants/{merchant_id}/purchases endpoint
           return await self._make_request(f"/merchants/{merchant_id}/purchases")
       except Exception as e:
           logger.error(f"Failed to fetch purchases for merchant {merchant_id}: {e}")
           raise Exception(f"Failed to fetch purchases for merchant {merchant_id}: {str(e)}")
  
   async def get_purchases_by_merchant_and_account(self, merchant_id: str, account_id: str) -> List[Dict[str, Any]]:
       """
       Fetch all purchases for a specific merchant and account combination
      
       Args:
           merchant_id (str): The merchant's unique identifier
           account_id (str): The account's unique identifier
          
       Returns:
           List[Dict[str, Any]]: List of purchase objects for this merchant and account
          
       Example:
           purchases = await service.get_purchases_by_merchant_and_account("507f1f77bcf86cd799439014", "507f1f77bcf86cd799439012")
       """
       try:
           # Make GET request to /merchants/{merchant_id}/accounts/{account_id}/purchases endpoint
           return await self._make_request(f"/merchants/{merchant_id}/accounts/{account_id}/purchases")
       except Exception as e:
           logger.error(f"Failed to fetch purchases for merchant {merchant_id} and account {account_id}: {e}")
           raise Exception(f"Failed to fetch purchases for merchant {merchant_id} and account {account_id}: {str(e)}")
  
   async def create_purchase(self, account_id: str, purchase_data: Dict[str, Any]) -> Dict[str, Any]:
       """
       Create a new transaction (purchase) for a specific account
      
       Args:
           account_id (str): The account to create the transaction for
           purchase_data (Dict[str, Any]): Transaction data to create
          
       Purchase Data Structure:
       {
           "merchant_id": "507f1f77bcf86cd799439014",  # Merchant ID (required)
           "medium": "balance",                        # Payment method (required)
           "purchase_date": "2023-10-04",            # Date (required)
           "amount": 23.45,                           # Amount (required)
           "description": "Coffee and pastry"         # Description (optional)
       }
      
       Returns:
           Dict[str, Any]: Created transaction object with assigned ID
          
       Example:
           new_purchase = {
               "merchant_id": "507f1f77bcf86cd799439014",
               "medium": "balance",
               "purchase_date": "2023-10-04",
               "amount": 15.99,
               "description": "Lunch"
           }
           result = await service.create_purchase("507f1f77bcf86cd799439012", new_purchase)
       """
       try:
           # Make POST request to /accounts/{account_id}/purchases endpoint with data
           return await self._make_request(f"/accounts/{account_id}/purchases", method="POST", data=purchase_data)
       except Exception as e:
           logger.error(f"Failed to create purchase: {e}")
           raise Exception(f"Failed to create purchase: {str(e)}")
  
   async def import_mock_data(self) -> Dict[str, Any]:
       """
       Import all available mock financial data from Nessie API
      
       This method performs a bulk import of all data types:
       - All customers in the system
       - All accounts across all customers
       - All transactions/purchases across all accounts
      
       The import runs in parallel for better performance, making multiple
       API calls simultaneously rather than sequentially.
      
       Returns:
           Dict[str, Any]: Import result with summary statistics
          
       Return Structure:
       {
           "success": True,
           "message": "Mock financial data imported successfully",
           "data": {
               "customers": [...],           # Array of customer objects
               "accounts": [...],            # Array of account objects 
               "transactions": [...],        # Array of transaction objects
               "summary": {
                   "customers_count": 5,     # Number of customers imported
                   "accounts_count": 12,     # Number of accounts imported
                   "transactions_count": 234, # Number of transactions imported
                   "total_balance": 15432.67  # Sum of all account balances
               }
           },
           "imported_at": "2023-10-04T12:00:00.000000"
       }
      
       Raises:
           Exception: If any of the API calls fail
          
       Example:
           result = await service.import_mock_data()
           print(f"Imported {result['data']['summary']['customers_count']} customers")
       """
       try:
           logger.info("Starting import of mock financial data from Nessie API")

           # Fetch all data types in parallel
           customers_task = self.get_customers()
           accounts_task = self.get_all_accounts()
           purchases_task = self.get_all_purchases()
          
           customers = await customers_task
           accounts = await accounts_task
           purchases = await purchases_task
          
           # Build comprehensive import result with data and statistics
           import_result = {
               "customers": customers,
               "accounts": accounts,
               "transactions": purchases,
               "summary": {
                   "customers_count": len(customers),
                   "accounts_count": len(accounts),
                   "transactions_count": len(purchases),
                   "total_balance": sum(float(acc.get("balance", 0)) for acc in accounts)
               }
           }

           logger.info(f"Successfully imported: {len(customers)} customers, {len(accounts)} accounts, {len(purchases)} transactions")
          
           return {
               "success": True,
               "message": "Mock financial data imported successfully",
               "data": import_result,        
               "imported_at": datetime.now().isoformat()
           }
          
       except Exception as e:
           logger.error(f"Failed to import mock data: {e}")
           raise Exception(f"Failed to import mock data: {str(e)}")

# Create a single instance of the NessieService that can be imported and used
# throughout the application. This ensures we reuse the same configuration
# and don't create multiple instances unnecessarily.
nessie_service = NessieService()
