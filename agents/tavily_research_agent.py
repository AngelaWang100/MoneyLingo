"""
Tavily MCP Server Integration for RealityCheck Financial Research
"""
import os
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

from .base_agent import BaseAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

class TavilyResearchAgent(BaseAgent):
    """
    Tavily-powered financial research agent using MCP Server endpoints
    Integrates Search, Extract, Crawl, and Map capabilities for financial data
    """
    
    def __init__(self):
        super().__init__(
            name="tavily_research_agent",
            description="Real-time financial research using Tavily MCP Server"
        )
        
        # Initialize Gemini for analysis
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.3
        )
        
        # Tavily MCP Server configuration
        self.tavily_api_key = "tvly-1234567890abcdef"  # Placeholder - replace with actual Tavily API key
        self.tavily_base_url = "https://api.tavily.com"
        
        # Financial research domains
        self.financial_domains = [
            "finance.yahoo.com",
            "marketwatch.com", 
            "bloomberg.com",
            "reuters.com",
            "cnbc.com",
            "investopedia.com",
            "sec.gov",
            "federalreserve.gov"
        ]
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process financial research request using Tavily MCP Server"""
        try:
            research_query = input_data.get("query", "")
            research_type = input_data.get("research_type", "general")
            language = input_data.get("language", "English")
            
            self.logger.info(f"Starting Tavily research for: {research_query}")
            
            # Determine research strategy based on type
            if research_type == "market_data":
                results = await self._research_market_data(research_query)
            elif research_type == "company_analysis":
                results = await self._research_company_analysis(research_query)
            elif research_type == "economic_indicators":
                results = await self._research_economic_indicators(research_query)
            elif research_type == "investment_news":
                results = await self._research_investment_news(research_query)
            else:
                results = await self._general_financial_research(research_query)
            
            # Analyze results with Gemini
            analysis = await self._analyze_research_results(results, research_query, language)
            
            # Log the research decision
            self.log_decision(
                decision=f"Completed Tavily research for: {research_query}",
                context={
                    "query": research_query,
                    "research_type": research_type,
                    "sources_found": len(results.get("sources", [])),
                    "tavily_success": results.get("success", False)
                },
                confidence=0.9
            )
            
            return {
                "success": True,
                "research_query": research_query,
                "research_type": research_type,
                "tavily_results": results,
                "ai_analysis": analysis,
                "sources": results.get("sources", []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Tavily research failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "research_query": input_data.get("query", ""),
                "timestamp": datetime.now().isoformat()
            }
    
    async def _research_market_data(self, query: str) -> Dict[str, Any]:
        """Research real-time market data using Tavily Search and Extract"""
        try:
            # Use Tavily Search for market data
            search_results = await self._tavily_search(
                query=f"{query} stock market data real-time",
                max_results=10,
                include_domains=self.financial_domains
            )
            
            # Extract specific data from top results
            extracted_data = []
            for result in search_results.get("results", [])[:3]:
                extracted = await self._tavily_extract(
                    url=result.get("url"),
                    query=f"Extract current price, change, volume for {query}"
                )
                if extracted.get("success"):
                    extracted_data.append(extracted)
            
            return {
                "success": True,
                "search_results": search_results,
                "extracted_data": extracted_data,
                "sources": [r.get("url") for r in search_results.get("results", [])]
            }
            
        except Exception as e:
            self.logger.error(f"Market data research failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _research_company_analysis(self, company: str) -> Dict[str, Any]:
        """Research company analysis using Tavily Search, Extract, and Crawl"""
        try:
            # Search for company information
            search_results = await self._tavily_search(
                query=f"{company} financial analysis earnings revenue",
                max_results=15,
                include_domains=self.financial_domains
            )
            
            # Crawl key financial pages
            crawled_data = []
            for result in search_results.get("results", [])[:5]:
                crawled = await self._tavily_crawl(
                    url=result.get("url"),
                    max_pages=3
                )
                if crawled.get("success"):
                    crawled_data.append(crawled)
            
            # Extract specific financial metrics
            extracted_metrics = []
            for crawl in crawled_data:
                extracted = await self._tavily_extract(
                    url=crawl.get("url"),
                    query=f"Extract revenue, profit, debt, market cap for {company}"
                )
                if extracted.get("success"):
                    extracted_metrics.append(extracted)
            
            return {
                "success": True,
                "search_results": search_results,
                "crawled_data": crawled_data,
                "extracted_metrics": extracted_metrics,
                "sources": [r.get("url") for r in search_results.get("results", [])]
            }
            
        except Exception as e:
            self.logger.error(f"Company analysis research failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _research_economic_indicators(self, indicator: str) -> Dict[str, Any]:
        """Research economic indicators using Tavily Search and Map"""
        try:
            # Search for economic data
            search_results = await self._tavily_search(
                query=f"{indicator} economic indicator current data",
                max_results=10,
                include_domains=["federalreserve.gov", "bls.gov", "bea.gov", "treasury.gov"]
            )
            
            # Map economic data geographically if relevant
            mapped_data = await self._tavily_map(
                query=f"Economic data for {indicator} by region",
                data_type="economic_indicators"
            )
            
            return {
                "success": True,
                "search_results": search_results,
                "mapped_data": mapped_data,
                "sources": [r.get("url") for r in search_results.get("results", [])]
            }
            
        except Exception as e:
            self.logger.error(f"Economic indicators research failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _research_investment_news(self, topic: str) -> Dict[str, Any]:
        """Research investment news using Tavily Search and Extract"""
        try:
            # Search for recent news
            search_results = await self._tavily_search(
                query=f"{topic} investment news analysis",
                max_results=20,
                include_domains=self.financial_domains
            )
            
            # Extract key insights from news articles
            extracted_insights = []
            for result in search_results.get("results", [])[:5]:
                extracted = await self._tavily_extract(
                    url=result.get("url"),
                    query=f"Extract key investment insights and market impact for {topic}"
                )
                if extracted.get("success"):
                    extracted_insights.append(extracted)
            
            return {
                "success": True,
                "search_results": search_results,
                "extracted_insights": extracted_insights,
                "sources": [r.get("url") for r in search_results.get("results", [])]
            }
            
        except Exception as e:
            self.logger.error(f"Investment news research failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _general_financial_research(self, query: str) -> Dict[str, Any]:
        """General financial research using all Tavily capabilities"""
        try:
            # Comprehensive search
            search_results = await self._tavily_search(
                query=query,
                max_results=15,
                include_domains=self.financial_domains
            )
            
            # Extract key information
            extracted_info = []
            for result in search_results.get("results", [])[:3]:
                extracted = await self._tavily_extract(
                    url=result.get("url"),
                    query=f"Extract key financial information related to: {query}"
                )
                if extracted.get("success"):
                    extracted_info.append(extracted)
            
            return {
                "success": True,
                "search_results": search_results,
                "extracted_info": extracted_info,
                "sources": [r.get("url") for r in search_results.get("results", [])]
            }
            
        except Exception as e:
            self.logger.error(f"General financial research failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _tavily_search(self, query: str, max_results: int = 10, include_domains: List[str] = None) -> Dict[str, Any]:
        """Use Tavily Search endpoint"""
        try:
            import httpx
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "search_depth": "advanced",
                "max_results": max_results,
                "include_domains": include_domains or [],
                "exclude_domains": ["wikipedia.org"],
                "include_answer": True,
                "include_raw_content": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.tavily_base_url}/search",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"success": False, "error": f"Search failed: {response.status_code}"}
                    
        except Exception as e:
            self.logger.error(f"Tavily search failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _tavily_extract(self, url: str, query: str) -> Dict[str, Any]:
        """Use Tavily Extract endpoint"""
        try:
            import httpx
            
            payload = {
                "api_key": self.tavily_api_key,
                "url": url,
                "query": query,
                "extract_content": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.tavily_base_url}/extract",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"success": False, "error": f"Extract failed: {response.status_code}"}
                    
        except Exception as e:
            self.logger.error(f"Tavily extract failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _tavily_crawl(self, url: str, max_pages: int = 3) -> Dict[str, Any]:
        """Use Tavily Crawl endpoint"""
        try:
            import httpx
            
            payload = {
                "api_key": self.tavily_api_key,
                "url": url,
                "max_pages": max_pages,
                "crawl_depth": "deep"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.tavily_base_url}/crawl",
                    json=payload,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"success": False, "error": f"Crawl failed: {response.status_code}"}
                    
        except Exception as e:
            self.logger.error(f"Tavily crawl failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _tavily_map(self, query: str, data_type: str) -> Dict[str, Any]:
        """Use Tavily Map endpoint for geographic data visualization"""
        try:
            import httpx
            
            payload = {
                "api_key": self.tavily_api_key,
                "query": query,
                "data_type": data_type,
                "visualization": True
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.tavily_base_url}/map",
                    json=payload,
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    return response.json()
                else:
                    return {"success": False, "error": f"Map failed: {response.status_code}"}
                    
        except Exception as e:
            self.logger.error(f"Tavily map failed: {e}")
            return {"success": False, "error": str(e)}
    
    async def _analyze_research_results(self, results: Dict[str, Any], query: str, language: str) -> str:
        """Analyze Tavily research results using Gemini"""
        try:
            # Prepare analysis prompt
            analysis_prompt = f"""
            Analyze this financial research data for the query: "{query}"
            
            Research Results:
            {json.dumps(results, indent=2)}
            
            Provide:
            1. Key findings and insights
            2. Market trends and patterns
            3. Risk assessment
            4. Investment recommendations
            5. Data reliability and source quality
            
            Respond in {language} with professional financial analysis.
            """
            
            messages = [
                SystemMessage(content="You are a senior financial analyst. Analyze the research data and provide comprehensive insights."),
                HumanMessage(content=analysis_prompt)
            ]
            
            response = await self.llm.ainvoke(messages)
            return response.content
            
        except Exception as e:
            self.logger.error(f"Research analysis failed: {e}")
            return f"Analysis failed: {str(e)}"
    
    async def get_research_capabilities(self) -> Dict[str, Any]:
        """Get available Tavily research capabilities"""
        return {
            "search": "Real-time financial data search",
            "extract": "Extract specific financial metrics",
            "crawl": "Deep crawl financial websites",
            "map": "Geographic financial data visualization",
            "domains": self.financial_domains,
            "supported_languages": ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Russian"]
        }
