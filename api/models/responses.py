# Defines the structure of API responses for PDF processing with LLM.

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class PDFProcessingResponse(BaseModel):
    """Response model for PDF processing operations"""
    success: bool = True
    message: str = "PDF processed successfully"
    timestamp: datetime = Field(default_factory=datetime.now)
    file_info: Optional[Dict[str, Any]] = None
    extracted_text: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None
    processing_time: Optional[float] = None


class PDFUploadRequest(BaseModel):
    """Request model for PDF upload and processing options"""
    analyze_with_llm: bool = True
    extract_text_only: bool = False
    custom_prompt: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    message: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    details: Optional[Dict[str, Any]] = None
