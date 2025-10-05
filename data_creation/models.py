# Data models for MoneyLingo financial explanation service

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime, date
from decimal import Decimal
from enum import Enum

class TransactionType(str, Enum):
    PURCHASE = "purchase"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    BILL_PAYMENT = "bill"
    LOAN_PAYMENT = "loan"

class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    CREDIT = "credit"
    LOAN = "loan"

class CustomerPreferences(BaseModel):
    """Customer language and communication preferences"""
    preferred_language: str = "en"
    voice_enabled: bool = True
    notification_preferences: Dict[str, bool] = Field(default_factory=dict)

class Address(BaseModel):
    """Address information"""
    street_number: str
    street_name: str
    city: str
    state: str
    zip_code: str
    country: str = "US"

class Customer(BaseModel):
    """Customer information"""
    _id: str
    first_name: str
    last_name: str
    email: str
    phone: str
    date_of_birth: date
    address: Address
    preferences: CustomerPreferences
    created_date: datetime
    last_login: Optional[datetime] = None

class Account(BaseModel):
    """Bank account information"""
    _id: str
    customer_id: str
    type: AccountType
    nickname: str
    account_number: str
    routing_number: str
    balance: float
    available_balance: float
    created_date: datetime
    status: str = "active"

class Merchant(BaseModel):
    """Merchant/vendor information"""
    _id: str
    name: str
    category: str
    address: Address
    phone: Optional[str] = None
    website: Optional[str] = None

class Transaction(BaseModel):
    """Base transaction model"""
    _id: str
    account_id: str
    type: TransactionType
    amount: float
    description: str
    date: datetime
    status: str = "completed"
    merchant_id: Optional[str] = None
    category: Optional[str] = None

class Purchase(Transaction):
    """Purchase transaction"""
    merchant_id: str
    type: TransactionType = TransactionType.PURCHASE


class Deposit(Transaction):
    """Deposit transaction"""
    type: TransactionType = TransactionType.DEPOSIT
    deposit_method: str  # "direct_deposit", "check", "cash", "transfer"

class Withdrawal(Transaction):
    """Withdrawal transaction"""
    type: TransactionType = TransactionType.WITHDRAWAL
    atm_id: Optional[str] = None
    fee: Optional[float] = None

class Transfer(Transaction):
    """Transfer transaction"""
    type: TransactionType = TransactionType.TRANSFER
    from_account_id: str
    to_account_id: str
    transfer_type: str  # "internal", "external", "wire"

class Bill(BaseModel):
    """Bill information"""
    _id: str
    account_id: str
    payee: str
    amount: float
    due_date: date
    status: str  # "pending", "paid", "overdue"
    category: str
    recurring: bool = False
    autopay: bool = False

class Loan(BaseModel):
    """Loan information"""
    _id: str
    account_id: str
    type: str  # "personal", "auto", "mortgage", "student"
    principal: float
    current_balance: float
    interest_rate: float
    monthly_payment: float
    due_date: date
    term_months: int
    status: str = "active"

class ATM(BaseModel):
    """ATM location information"""
    _id: str
    name: str
    address: Address
    available_24_7: bool = True
    services: List[str] = Field(default_factory=list)

class Branch(BaseModel):
    """Bank branch information"""
    _id: str
    name: str
    address: Address
    phone: str
    hours: Dict[str, str] = Field(default_factory=dict)
    services: List[str] = Field(default_factory=list)
