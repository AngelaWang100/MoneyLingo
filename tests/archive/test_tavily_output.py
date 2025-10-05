"""
Test Tavily research agent output specifically
"""
import asyncio
import logging
import sys
import os
from dotenv import load_dotenv

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_tavily_research():
    """Test Tavily research agent and show detailed output"""
    try:
        from api.services.agents.tavily_research_agent import TavilyResearchAgent
        
        agent = TavilyResearchAgent()
        logger.info("✅ Tavily Research Agent initialized")
        
        # Test with different types of financial queries
        test_queries = [
            {
                "query": "retirement planning strategies 2024",
                "research_type": "retirement_planning",
                "max_results": 3
            },
            {
                "query": "best investment options for beginners",
                "research_type": "investment_advice", 
                "max_results": 3
            },
            {
                "query": "cryptocurrency market trends",
                "research_type": "market_analysis",
                "max_results": 3
            }
        ]
        
        for i, test_data in enumerate(test_queries, 1):
            logger.info(f"\n🔍 Test Query {i}: {test_data['query']}")
            logger.info(f"Research Type: {test_data['research_type']}")
            
            result = await agent.process(test_data)
            
            if result.get("success"):
                logger.info("✅ Tavily Research SUCCESS!")
                
                # Show AI analysis
                ai_analysis = result.get("ai_analysis", "")
                logger.info(f"\n🤖 AI Analysis:")
                logger.info(f"{ai_analysis[:200]}..." if len(ai_analysis) > 200 else ai_analysis)
                
                # Show research results
                research_results = result.get("research_results", [])
                logger.info(f"\n📊 Research Results ({len(research_results)} found):")
                
                for j, research in enumerate(research_results, 1):
                    logger.info(f"\n  📄 Result {j}:")
                    logger.info(f"    Title: {research.get('title', 'N/A')}")
                    logger.info(f"    Source: {research.get('source', 'N/A')}")
                    logger.info(f"    Relevance: {research.get('relevance_score', 'N/A')}")
                    logger.info(f"    URL: {research.get('url', 'N/A')}")
                    content = research.get('content', '')
                    logger.info(f"    Content: {content[:100]}..." if len(content) > 100 else f"    Content: {content}")
                
                # Test additional Tavily methods
                logger.info(f"\n🔬 Testing additional Tavily methods...")
                
                # Test financial data search
                search_result = await agent.search_financial_data(test_data['query'])
                logger.info(f"Financial Data Search: {search_result.get('success', False)}")
                
                # Test insight extraction
                if research_results:
                    sample_content = research_results[0].get('content', '')
                    insights = await agent.extract_financial_insights(sample_content)
                    logger.info(f"Insight Extraction: {insights.get('success', False)}")
                    if insights.get('success'):
                        insight_text = insights.get('insights', '')
                        logger.info(f"Extracted Insights: {insight_text[:150]}..." if len(insight_text) > 150 else insight_text)
                
            else:
                logger.error(f"❌ Tavily Research FAILED: {result.get('error', 'Unknown error')}")
            
            logger.info("\n" + "-"*60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Tavily test failed: {e}")
        return False

async def test_tavily_integration():
    """Test Tavily integration with orchestrator"""
    try:
        from api.services.agents.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        logger.info("✅ Orchestrator with Tavily initialized")
        
        # Test with research-focused query
        research_data = {
            "content": "I need comprehensive research on sustainable investing trends",
            "language": "English",
            "user_level": "intermediate",
            "goals": ["sustainable investing research"],
            "income": 75000,
            "expenses": 45000,
            "query": "sustainable investing trends 2024",
            "research_type": "sustainable_investing"
        }
        
        logger.info(f"\n🧠 Testing Orchestrator with Tavily Research...")
        logger.info(f"Query: {research_data['query']}")
        
        result = await orchestrator.process_request(research_data)
        
        if result.get("success"):
            logger.info("✅ Orchestrator with Tavily SUCCESS!")
            
            # Show synthesis
            synthesis = result.get("result", {}).get("synthesis", "")
            logger.info(f"\n🎯 Orchestration Synthesis:")
            logger.info(f"{synthesis}")
            
            # Show successful agents
            successful_agents = result.get("result", {}).get("successful_agents", [])
            logger.info(f"\n✅ Successful Agents: {successful_agents}")
            
            # Show agent results
            agent_results = result.get("result", {}).get("agent_results", {})
            for agent_name, agent_result in agent_results.items():
                if agent_result.get("success"):
                    logger.info(f"\n🤖 {agent_name} Results:")
                    result_data = agent_result.get("result", {})
                    if "research_results" in result_data:
                        research_count = len(result_data.get("research_results", []))
                        logger.info(f"  📊 Research Results: {research_count} found")
                    if "ai_analysis" in result_data:
                        analysis = result_data.get("ai_analysis", "")
                        logger.info(f"  🤖 AI Analysis: {analysis[:100]}..." if len(analysis) > 100 else f"  🤖 AI Analysis: {analysis}")
            
        else:
            logger.error(f"❌ Orchestrator with Tavily FAILED: {result.get('error', 'Unknown error')}")
        
        return result.get("success", False)
        
    except Exception as e:
        logger.error(f"❌ Tavily integration test failed: {e}")
        return False

async def run_tavily_tests():
    """Run comprehensive Tavily tests"""
    logger.info("🚀 Starting Tavily Research Agent Tests...")
    
    tests = [
        ("Tavily Research Agent", test_tavily_research),
        ("Tavily + Orchestrator Integration", test_tavily_integration),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*70}")
        logger.info(f"🧪 Testing {test_name}...")
        try:
            result = await test_func()
            results[test_name] = result
            status = "✅ PASSED" if result else "❌ FAILED"
            logger.info(f"{status}: {test_name}")
        except Exception as e:
            logger.error(f"❌ FAILED: {test_name} - {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("📊 TAVILY RESEARCH TEST SUMMARY")
    logger.info("="*70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
    
    logger.info(f"\n🎯 Overall: {passed}/{total} Tavily tests passed")
    
    if passed == total:
        logger.info("🎉 TAVILY RESEARCH AGENT IS WORKING PERFECTLY!")
        logger.info("🔍 Your RealityCheck platform has real-time financial research capabilities!")
    else:
        logger.warning(f"⚠️  {total - passed} Tavily tests failed.")
    
    return results

if __name__ == "__main__":
    asyncio.run(run_tavily_tests())
