# Generates realistic financial data for MoneyLingo testing and demos

import random
import string
from datetime import datetime, date, timedelta
from typing import List, Dict, Any
from faker import Faker
import uuid

# Initialize Faker for US English only
fake = Faker('en_US')

class MoneyLingoDataGenerator:
    """Generates realistic financial data for MoneyLingo"""
    
    def __init__(self):
        self.customers = []
        self.accounts = []
        self.merchants = []
        self.transactions = []
        self.bills = []
        self.loans = []
        self.atms = []
        self.branches = []
        
        # Predefined data for consistency
        self.transaction_categories = [
            "Groceries", "Gas", "Restaurants", "Shopping", "Entertainment",
            "Bills", "Healthcare", "Education", "Travel", "Subscriptions",
            "Insurance", "Utilities", "Rent/Mortgage", "ATM Fees", "Bank Fees"
        ]
        
        self.merchant_categories = [
            "Grocery Store", "Gas Station", "Restaurant", "Retail", "Online",
            "Pharmacy", "Medical", "Entertainment", "Subscription Service",
            "Utility Company", "Insurance", "Government", "Bank"
        ]
        
        self.languages = [
            "en"  # English only
        ]
        
        self.account_types = ["checking", "savings", "credit", "loan"]

        # Real US cities and states (from gisgeography.com)
        self.real_cities_states = [
            ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"),
            ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"),
            ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"),
            ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("San Francisco", "CA"),
            ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"), ("Washington", "DC"),
            ("Boston", "MA"), ("El Paso", "TX"), ("Nashville", "TN"), ("Detroit", "MI"),
            ("Oklahoma City", "OK"), ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"),
            ("Louisville", "KY"), ("Baltimore", "MD"), ("Milwaukee", "WI"), ("Albuquerque", "NM"),
            ("Tucson", "AZ"), ("Fresno", "CA"), ("Mesa", "AZ"), ("Sacramento", "CA"),
            ("Atlanta", "GA"), ("Kansas City", "MO"), ("Colorado Springs", "CO"), ("Miami", "FL"),
            ("Raleigh", "NC"), ("Omaha", "NE"), ("Long Beach", "CA"), ("Virginia Beach", "VA"),
            ("Oakland", "CA"), ("Minneapolis", "MN"), ("Tulsa", "OK"), ("Tampa", "FL"),
            ("Arlington", "TX"), ("New Orleans", "LA"), ("Wichita", "KS"), ("Cleveland", "OH"),
            ("Bakersfield", "CA"), ("Aurora", "CO"), ("Anaheim", "CA"), ("Honolulu", "HI"),
            ("Santa Ana", "CA"), ("Riverside", "CA"), ("Corpus Christi", "TX"), ("Lexington", "KY"),
            ("Stockton", "CA"), ("Henderson", "NV"), ("Saint Paul", "MN"), ("St. Louis", "MO"),
            ("Cincinnati", "OH"), ("Pittsburgh", "PA"), ("Greensboro", "NC"), ("Anchorage", "AK"),
            ("Plano", "TX"), ("Lincoln", "NE"), ("Orlando", "FL"), ("Irvine", "CA"),
            ("Newark", "NJ"), ("Durham", "NC"), ("Chula Vista", "CA"), ("Toledo", "OH"),
            ("Fort Wayne", "IN"), ("St. Petersburg", "FL"), ("Laredo", "TX"), ("Jersey City", "NJ"),
            ("Chandler", "AZ"), ("Madison", "WI"), ("Lubbock", "TX"), ("Norfolk", "VA"),
            ("Baton Rouge", "LA"), ("Spokane", "WA"), ("Des Moines", "IA"), ("Fremont", "CA"),
            ("Richmond", "VA"), ("Santa Clarita", "CA"), ("Miami Gardens", "FL"), ("Pearland", "TX"),
            ("Fayetteville", "NC"), ("Birmingham", "AL"), ("Eugene", "OR"), ("Tacoma", "WA"),
            ("Huntsville", "AL"), ("Shreveport", "LA"), ("Mobile", "AL"), ("Little Rock", "AR"),
            ("Augusta", "GA"), ("Amarillo", "TX"), ("Glendale", "AZ"), ("Columbus", "GA"),
            ("Grand Rapids", "MI"), ("Salt Lake City", "UT"), ("Tallahassee", "FL"), ("Worcester", "MA"),
            ("Newport News", "VA"), ("Huntington Beach", "CA"), ("Knoxville", "TN"), ("Providence", "RI")
        ]
    
    def generate_customer_id(self) -> str:
        """Generate a unique customer ID"""
        return f"CUST_{uuid.uuid4().hex[:8].upper()}"
    
    def generate_account_id(self) -> str:
        """Generate a unique account ID"""
        return f"ACC_{uuid.uuid4().hex[:8].upper()}"
    
    def generate_transaction_id(self) -> str:
        """Generate a unique transaction ID"""
        return f"TXN_{uuid.uuid4().hex[:10].upper()}"
    
    def generate_address(self) -> Dict[str, str]:
        """Generate a realistic address with real US cities"""
        city, state = random.choice(self.real_cities_states)
        return {
            "street_number": str(fake.building_number()),
            "street_name": fake.street_name(),
            "city": city,
            "state": state,
            "zip": fake.zipcode()
        }

    def generate_customers(self, num_customers: int = 50):
        """Generate customer data"""
        customers = []
        for _ in range(num_customers):
            customer = {
                "_id": self.generate_customer_id(),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "address": self.generate_address(),
            }
            customers.append(customer)
        self.customers = customers
        return customers

    def generate_accounts(self, accounts_per_customer: int = 2):
        """Generate a number of random accounts for the customers"""
        
        # Ensure customers are generated first
        if not self.customers:
            self.generate_customers()
            
        for customer in self.customers:
            num_accounts = random.randint(1, 4)
            
            for _ in range(num_accounts):
                account_type = random.choice(["Savings", "Checking", "Credit Card"])
                
                account = {
                    "_id": self.generate_account_id(),
                    "type": account_type,
                    "nickname": f"{customer['first_name']}'s {account_type}",
                    "rewards": 0,
                    "balance": round(random.uniform(50.0, 10000.0), 2),
                    "account_number": fake.credit_card_number(),
                    "customer_id": customer['_id']
                }
                self.accounts.append(account)
        
        print(f"Generated {len(self.accounts)} accounts")
        return self.accounts

    def generate_merchants(self, num_merchants: int = 100):
        """Generate a number of random merchants"""
        for _ in range(num_merchants):
            merchant = {
                "_id": f"MERCH_{uuid.uuid4().hex[:8].upper()}",
                "name": fake.company(),
                "category": random.choice(self.merchant_categories),
                "address": self.generate_address()
            }
            self.merchants.append(merchant)
        
        print(f"Generated {len(self.merchants)} merchants")
        return self.merchants

    def generate_confusing_transaction_descriptions(self) -> str:
        """Generate confusing transaction descriptions that MoneyLingo should explain"""
        confusing_descriptions = [
            "SQ *COFFEE SHOP 123 San Francisco CA",
            "PAYPAL *AMAZON.COM 402-935-7733 WA",
            "SP * NETFLIX.COM 866-579-7172 CA",
            "TST* UBER TRIP 415-555-0123 CA",
            "CHECKCARD PURCHASE POS 1234567890123456",
            "ACH WITHDRAWAL 1234567890 AUTOPAY",
            "ZELLE PAYMENT TO JOHN DOE",
            "VENMO PAYMENT 4029357733",
            "CASHAPP *PAYMENT 1234567890",
            "APL*APPLE.COM/BILL 866-712-7753 CA",
            "AMZN Mktp US*ABC123DEF Amazon.com WA",
            "POS PURCHASE - VISA CHECK CARD",
            "OVERDRAFT FEE CHARGED ON 01/15",
            "MONTHLY MAINTENANCE FEE",
            "FOREIGN TRANSACTION FEE",
            "ATM WITHDRAWAL FEE NON-NETWORK",
            "RECURRING DEBIT CARD PURCHASE",
            "ACH CREDIT PAYROLL DEPOSIT",
            "WIRE TRANSFER INCOMING",
            "MOBILE DEPOSIT ITEM RETURNED"
        ]
        
        return random.choice(confusing_descriptions)
    
    def generate_transactions(self):
        """Generate transaction history"""
        for account in self.accounts:
            # Generate 10-100 transactions per account
            num_transactions = random.randint(10, 100)
            
            for _ in range(num_transactions):
                transaction_type = random.choice(["purchase", "deposit", "withdrawal", "transfer", "bill"])
                
                # Generate amount based on transaction type
                if transaction_type == "purchase":
                    amount = round(random.uniform(5, 500), 2)
                elif transaction_type == "deposit":
                    amount = round(random.uniform(100, 5000), 2)
                elif transaction_type == "withdrawal":
                    amount = round(random.uniform(20, 300), 2)
                elif transaction_type == "transfer":
                    amount = round(random.uniform(50, 1000), 2)
                else:  # bill
                    amount = round(random.uniform(25, 800), 2)
                
                transaction = {
                    "_id": self.generate_transaction_id(),
                    "account_id": account["_id"],
                    "type": transaction_type,
                    "amount": amount,
                    "description": self.generate_confusing_transaction_descriptions(),
                    "date": fake.date_time_between(start_date='-6m', end_date='now').isoformat(),
                    "status": random.choice(["completed", "completed", "completed", "pending"]),
                    "merchant_id": random.choice(self.merchants)["_id"] if transaction_type == "purchase" else None,
                    "category": random.choice(self.transaction_categories)
                }
                
                self.transactions.append(transaction)
        
        print(f"Generated {len(self.transactions)} transactions")
        return self.transactions
    
    def generate_bills(self, accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate bills for accounts"""
        bills = []
        
        bill_payees = [
            "Electric Company", "Gas Company", "Water Department", "Internet Provider",
            "Cable TV", "Mobile Phone", "Insurance Co", "Credit Card", "Mortgage Lender",
            "Car Payment", "Student Loans", "Gym Membership", "Netflix", "Spotify"
        ]
        
        for account in accounts:
            if account["type"] in ["checking", "savings"]:
                # Generate 3-8 bills per account
                num_bills = random.randint(3, 8)
                
                for _ in range(num_bills):
                    bill = {
                        "_id": f"BILL_{uuid.uuid4().hex[:8].upper()}",
                        "account_id": account["_id"],
                        "payee": random.choice(bill_payees),
                        "amount": round(random.uniform(25, 800), 2),
                        "due_date": (datetime.now() + timedelta(days=random.randint(-30, 30))).date().isoformat(),
                        "status": random.choice(["pending", "paid", "overdue"]),
                        "category": random.choice(self.transaction_categories),
                        "recurring": random.choice([True, False]),
                        "autopay": random.choice([True, False])
                    }
                    
                    bills.append(bill)
        
        self.bills = bills
        return bills
    
    def generate_loans(self, accounts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate loan data"""
        loans = []
        
        loan_types = ["personal", "auto", "mortgage", "student"]
        
        for account in accounts:
            if random.choice([True, False, False]):  # Not everyone has loans
                loan_type = random.choice(loan_types)
                
                # Different loan amounts by type
                if loan_type == "mortgage":
                    principal = round(random.uniform(200000, 800000), 2)
                    term_months = random.choice([180, 240, 300, 360])  # 15-30 years
                elif loan_type == "auto":
                    principal = round(random.uniform(15000, 60000), 2)
                    term_months = random.choice([36, 48, 60, 72])  # 3-6 years
                elif loan_type == "student":
                    principal = round(random.uniform(10000, 100000), 2)
                    term_months = random.choice([120, 180, 240])  # 10-20 years
                else:  # personal
                    principal = round(random.uniform(5000, 50000), 2)
                    term_months = random.choice([24, 36, 48, 60])  # 2-5 years
                
                current_balance = principal * random.uniform(0.3, 0.95)  # Partially paid off
                interest_rate = round(random.uniform(3.5, 18.0), 2)
                
                loan = {
                    "_id": f"LOAN_{uuid.uuid4().hex[:8].upper()}",
                    "account_id": account["_id"],
                    "type": loan_type,
                    "principal": principal,
                    "current_balance": round(current_balance, 2),
                    "interest_rate": interest_rate,
                    "monthly_payment": round((current_balance * (interest_rate/100/12)) / (1 - (1 + interest_rate/100/12)**(-term_months)), 2),
                    "due_date": (datetime.now() + timedelta(days=random.randint(1, 30))).date().isoformat(),
                    "term_months": term_months,
                    "status": random.choice(["active", "active", "active", "delinquent"])
                }
                
                loans.append(loan)
        
        self.loans = loans
        return loans
    
    def generate_atms(self, count: int = 25) -> List[Dict[str, Any]]:
        """Generate ATM locations"""
        atms = []
        
        for _ in range(count):
            atm = {
                "_id": f"ATM_{uuid.uuid4().hex[:8].upper()}",
                "name": f"ATM - {fake.street_name()}",
                "address": self.generate_address(),
                "available_24_7": random.choice([True, False]),
                "services": random.sample([
                    "Cash Withdrawal", "Balance Inquiry", "Deposit", 
                    "Transfer", "Mini Statement"
                ], random.randint(2, 5))
            }
            
            atms.append(atm)
        
        self.atms = atms
        return atms
    
    def generate_branches(self, count: int = 10) -> List[Dict[str, Any]]:
        """Generate bank branch locations"""
        branches = []
        
        for _ in range(count):
            branch = {
                "_id": f"BRANCH_{uuid.uuid4().hex[:8].upper()}",
                "name": f"MoneyLingo Bank - {fake.city()}",
                "address": self.generate_address(),
                "phone": fake.phone_number(),
                "hours": {
                    "Monday": "9:00 AM - 5:00 PM",
                    "Tuesday": "9:00 AM - 5:00 PM", 
                    "Wednesday": "9:00 AM - 5:00 PM",
                    "Thursday": "9:00 AM - 5:00 PM",
                    "Friday": "9:00 AM - 6:00 PM",
                    "Saturday": "9:00 AM - 2:00 PM",
                    "Sunday": "Closed"
                },
                "services": [
                    "Personal Banking", "Business Banking", "Loans", 
                    "Investment Services", "Safe Deposit Boxes", "Notary"
                ]
            }
            
            branches.append(branch)
        
        self.branches = branches
        return branches
    
    def generate_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate all data types and return as a dictionary"""
        print("Generating financial data...")
        
        customers = self.generate_customers(50)
        print(f"Generated {len(self.customers)} customers")
        
        self.generate_accounts()
        print(f"Generated {len(self.accounts)} accounts")
        
        merchants = self.generate_merchants(100)
        print(f"Generated {len(self.merchants)} merchants")
        
        transactions = self.generate_transactions()
        print(f"Generated {len(self.transactions)} transactions")
        
        bills = self.generate_bills(self.accounts)
        print(f"Generated {len(self.bills)} bills")
        
        loans = self.generate_loans(self.accounts)
        print(f"Generated {len(self.loans)} loans")
        
        atms = self.generate_atms(25)
        print(f"Generated {len(self.atms)} ATMs")
        
        branches = self.generate_branches(10)
        print(f"Generated {len(self.branches)} branches")
        
        return {
            "customers": self.customers,
            "accounts": self.accounts,
            "merchants": self.merchants,
            "transactions": self.transactions,
            "bills": self.bills,
            "loans": self.loans,
            "atms": self.atms,
            "branches": self.branches
        }
