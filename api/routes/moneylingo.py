# Provides API endpoints for MoneyLingo, explaining financial transactions in plain language
# and provides multi-language support.

from fastapi import APIRouter, HTTPException, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
import logging

# Import data models and services
from api.models.responses import PDFProcessingResponse, ErrorResponse
from api.services.translation_service import translation_service
from api.services.llm_service import llm_service
from api.services.pdf_service_new import pdf_service
from api.dependencies.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()

# Load generated financial data
def load_financial_data():
    """Load the generated financial data from individual JSON files."""
    data = {}
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    data_dir = os.path.join(base_dir, "data_creation", "generated_data")
    try:
        for filename in os.listdir(data_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(data_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Use the filename without extension as the key
                    key = os.path.splitext(filename)[0]
                    data[key] = json.load(f)
        return {"data": data}
    except Exception as e:
        logger.error(f"Failed to load financial data: {e}")
        return {"data": {}}

# Global data store
FINANCIAL_DATA = load_financial_data()

@router.get("/customers")
async def get_all_customers(current_user: dict = Depends(get_current_user)):
    """Get all customers"""
    try:
        customers = FINANCIAL_DATA.get("data", {}).get("customers", [])
        return {
            "success": True,
            "message": f"Retrieved {len(customers)} customers",
            "data": customers,
            "count": len(customers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customers: {str(e)}")

@router.get("/customers/{customer_id}")
async def get_customer(customer_id: str, current_user: dict = Depends(get_current_user)):
    """Get customer by ID"""
    try:
        customers = FINANCIAL_DATA.get("data", {}).get("customers", [])
        customer = next((c for c in customers if c["_id"] == customer_id), None)
        
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        return {
            "success": True,
            "message": "Customer retrieved successfully",
            "data": customer
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customer: {str(e)}")

@router.post("/customers")
async def create_customer(customer_data: Dict[str, Any]):
    """Create a new customer"""
    return {
        "success": True,
        "message": "Customer created successfully",
        "data": customer_data
    }

@router.get("/accounts")
async def get_all_accounts(current_user: dict = Depends(get_current_user)):
    """Get all accounts"""
    try:
        accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
        return {
            "success": True,
            "message": f"Retrieved {len(accounts)} accounts",
            "data": accounts,
            "count": len(accounts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get accounts: {str(e)}")

@router.get("/accounts/{account_id}")
async def get_account(account_id: str):
    """Get account by ID"""
    try:
        accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
        account = next((a for a in accounts if a["_id"] == account_id), None)
        
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        return {
            "success": True,
            "message": "Account retrieved successfully", 
            "data": account
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get account: {str(e)}")

@router.get("/customers/{customer_id}/accounts")
async def get_customer_accounts(customer_id: str):
    """Get accounts by customer ID"""
    try:
        accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
        customer_accounts = [a for a in accounts if a["customer_id"] == customer_id]
        
        return {
            "success": True,
            "message": f"Retrieved {len(customer_accounts)} accounts for customer",
            "data": customer_accounts,
            "count": len(customer_accounts)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customer accounts: {str(e)}")

@router.get("/accounts/{account_id}/purchases")
async def get_account_purchases(account_id: str):
    """Get all purchases for an account"""
    try:
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        purchases = [t for t in transactions if t["account_id"] == account_id and t["type"] == "purchase"]
        
        return {
            "success": True,
            "message": f"Retrieved {len(purchases)} purchases",
            "data": purchases,
            "count": len(purchases)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get purchases: {str(e)}")

@router.get("/accounts/{account_id}/deposits")
async def get_account_deposits(account_id: str):
    """Get all deposits for an account"""
    try:
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        deposits = [t for t in transactions if t["account_id"] == account_id and t["type"] == "deposit"]
        
        return {
            "success": True,
            "message": f"Retrieved {len(deposits)} deposits",
            "data": deposits,
            "count": len(deposits)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get deposits: {str(e)}")

@router.get("/accounts/{account_id}/withdrawals")
async def get_account_withdrawals(account_id: str):
    """Get all withdrawals for an account"""
    try:
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        withdrawals = [t for t in transactions if t["account_id"] == account_id and t["type"] == "withdrawal"]
        
        return {
            "success": True,
            "message": f"Retrieved {len(withdrawals)} withdrawals",
            "data": withdrawals,
            "count": len(withdrawals)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get withdrawals: {str(e)}")

@router.get("/accounts/{account_id}/transfers")
async def get_account_transfers(account_id: str):
    """Get all transfers for an account"""
    try:
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        transfers = [t for t in transactions if t["account_id"] == account_id and t["type"] == "transfer"]
        
        return {
            "success": True,
            "message": f"Retrieved {len(transfers)} transfers",
            "data": transfers,
            "count": len(transfers)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get transfers: {str(e)}")

@router.get("/accounts/{account_id}/bills")
async def get_account_bills(account_id: str):
    """Get all bills for an account"""
    try:
        bills = FINANCIAL_DATA.get("data", {}).get("bills", [])
        account_bills = [b for b in bills if b["account_id"] == account_id]
        
        return {
            "success": True,
            "message": f"Retrieved {len(account_bills)} bills",
            "data": account_bills,
            "count": len(account_bills)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get bills: {str(e)}")

@router.get("/customers/{customer_id}/bills")
async def get_customer_bills(customer_id: str):
    """Get bills by customer ID"""
    try:
        # FGet customer's accounts
        accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
        customer_account_ids = [a["_id"] for a in accounts if a["customer_id"] == customer_id]
        
        # Then get bills for those accounts
        bills = FINANCIAL_DATA.get("data", {}).get("bills", [])
        customer_bills = [b for b in bills if b["account_id"] in customer_account_ids]
        
        return {
            "success": True,
            "message": f"Retrieved {len(customer_bills)} bills for customer",
            "data": customer_bills,
            "count": len(customer_bills)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customer bills: {str(e)}")

@router.get("/accounts/{account_id}/loans")
async def get_account_loans(account_id: str):
    """Get all loans for an account"""
    try:
        loans = FINANCIAL_DATA.get("data", {}).get("loans", [])
        account_loans = [l for l in loans if l["account_id"] == account_id]
        
        return {
            "success": True,
            "message": f"Retrieved {len(account_loans)} loans",
            "data": account_loans,
            "count": len(account_loans)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get loans: {str(e)}")

@router.get("/merchants")
async def get_all_merchants():
    """Get all merchants"""
    try:
        merchants = FINANCIAL_DATA.get("data", {}).get("merchants", [])
        return {
            "success": True,
            "message": f"Retrieved {len(merchants)} merchants",
            "data": merchants,
            "count": len(merchants)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get merchants: {str(e)}")

@router.get("/merchants/{merchant_id}")
async def get_merchant(merchant_id: str):
    """Get merchant by ID"""
    try:
        merchants = FINANCIAL_DATA.get("data", {}).get("merchants", [])
        merchant = next((m for m in merchants if m["_id"] == merchant_id), None)
        
        if not merchant:
            raise HTTPException(status_code=404, detail="Merchant not found")
        
        return {
            "success": True,
            "message": "Merchant retrieved successfully",
            "data": merchant
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get merchant: {str(e)}")

@router.get("/atms")
async def get_all_atms():
    """Get all ATMs"""
    try:
        atms = FINANCIAL_DATA.get("data", {}).get("atms", [])
        return {
            "success": True,
            "message": f"Retrieved {len(atms)} ATMs",
            "data": atms,
            "count": len(atms)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get ATMs: {str(e)}")

@router.get("/branches")
async def get_all_branches():
    """Get all branches"""
    try:
        branches = FINANCIAL_DATA.get("data", {}).get("branches", [])
        return {
            "success": True,
            "message": f"Retrieved {len(branches)} branches",
            "data": branches,
            "count": len(branches)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get branches: {str(e)}")

@router.post("/explain-transaction")
async def explain_transaction(
    transaction_id: str = Form(...),
    language: str = Form(default="en"),
    voice_response: bool = Form(default=False),
    current_user: dict = Depends(get_current_user)
):
    """
    Explain a confusing transaction in plain language (core MoneyLingo feature)
    """
    try:
        # Find the transaction
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        transaction = next((t for t in transactions if t["_id"] == transaction_id), None)
        
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        # Generate explanation using LLM
        explanation = await llm_service.explain_transaction(transaction)
        
        # Translate if needed
        if language != "en":
            explanation = await translation_service.translate_text(explanation, target_language=language)
        
        response_data = {
            "transaction": transaction,
            "explanation": explanation,
            "language": language,
            "plain_language_summary": explanation
        }
        
        # Add voice response if requested
        if voice_response:
            # TODO: Implement text-to-speech
            response_data["audio_url"] = f"/audio/explanation_{transaction_id}_{language}.mp3"
        
        return {
            "success": True,
            "message": "Transaction explained successfully",
            "data": response_data
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to explain transaction: {str(e)}")

@router.post("/upload-pdf", response_model=PDFProcessingResponse)
async def upload_and_process_pdf(
    file: UploadFile = File(...),
    language: str = Form(default="en"),
    explain_transactions: bool = Form(default=True),
    voice_response: bool = Form(default=False),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload PDF financial document (bank statements, bills, etc.) and get explanations (core MoneyLingo feature).
    """
    try:
        # Process the PDF
        pdf_result = await pdf_service.process_pdf(file)
        
        explanations = []
        if explain_transactions and pdf_result.get("transactions"):
            # Explain each transaction found in the PDF
            for transaction in pdf_result["transactions"]:
                explanation = await llm_service.explain_transaction_text(transaction)
                
                if language != "en":
                    explanation = await translation_service.translate_text(explanation, target_language=language)
                
                explanations.append({
                    "transaction": transaction,
                    "explanation": explanation
                })
        
        response_data = {
            "file_info": {
                "filename": file.filename,
                "size": file.size,
                "content_type": file.content_type
            },
            "extracted_text": pdf_result.get("text", ""),
            "analysis": {
                "transactions_found": len(pdf_result.get("transactions", [])),
                "explanations": explanations,
                "language": language
            }
        }
        
        return PDFProcessingResponse(
            success=True,
            message="PDF processed and transactions explained successfully",
            file_info=response_data["file_info"],
            extracted_text=response_data["extracted_text"],
            analysis=response_data["analysis"],
            processing_time=pdf_result.get("processing_time", 0)
        )
        
    except Exception as e:
        logger.error(f"PDF processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process PDF: {str(e)}")

@router.post("/ask-question")
async def ask_financial_question(
    question: str = Form(...),
    customer_id: Optional[str] = Form(default=None),
    language: str = Form(default="en"),
    voice_response: bool = Form(default=False),
    current_user: dict = Depends(get_current_user)
):
    """
    Ask questions about finances in natural language.
    """
    try:
        # Get customer data if provided
        customer_context = {}
        if customer_id:
            # Get customer's accounts and transactions
            accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
            transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
            
            customer_accounts = [a for a in accounts if a["customer_id"] == customer_id]
            customer_account_ids = [a["_id"] for a in customer_accounts]
            customer_transactions = [t for t in transactions if t["account_id"] in customer_account_ids]
            
            customer_context = {
                "accounts": customer_accounts,
                "transactions": customer_transactions[-50:] # Last 50 transactions
            }
        
        # Generate answer using LLM
        answer = await llm_service.answer_financial_question(question, customer_context)
        
        # Translate if needed
        if language != "en":
            answer = await translation_service.translate_text(answer, target_language=language)
        
        response_data = {
            "question": question,
            "answer": answer,
            "language": language,
            "has_customer_context": bool(customer_id)
        }
        
        # Add voice response if requested
        if voice_response:
            # TODO: Implement text-to-speech
            response_data["audio_url"] = f"/audio/answer_{hash(question)}_{language}.mp3"
        
        return {
            "success": True,
            "message": "Question answered successfully",
            "data": response_data
        }
        
    except Exception as e:
        logger.error(f"Question answering failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to answer question: {str(e)}")

@router.get("/spending-summary/{customer_id}")
async def get_spending_summary(
    customer_id: str,
    language: str = "en",
    months: int = 6,
    current_user: dict = Depends(get_current_user)
):
    """
    Get a spending summary with explanations for a customer
    """
    try:
        # Get customer's transactions
        accounts = FINANCIAL_DATA.get("data", {}).get("accounts", [])
        transactions = FINANCIAL_DATA.get("data", {}).get("transactions", [])
        
        customer_accounts = [a for a in accounts if a["customer_id"] == customer_id]
        customer_account_ids = [a["_id"] for a in customer_accounts]
        customer_transactions = [t for t in transactions if t["account_id"] in customer_account_ids]
        
        # Generate spending analysis
        analysis = await llm_service.generate_spending_analysis(customer_transactions)
        
        # Translate if needed
        if language != "en":
            analysis["summary"] = await translation_service.translate_text(analysis["summary"], target_language=language)
        
        return {
            "success": True,
            "message": "Spending summary generated successfully",
            "data": analysis
        }
        
    except Exception as e:
        logger.error(f"Spending summary failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate spending summary: {str(e)}")
