"""
Demo script to test all agents end-to-end
"""
import asyncio
import json
import logging
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.orchestrator import AgentOrchestrator
from observability.comet_integration import CometObserver

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentDemo:
    """Demo class for testing all agents"""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.observer = CometObserver()
        self.results = []
    
    async def test_translation_agent(self):
        """Test translation agent with sample data"""
        logger.info("Testing Translation Agent...")
        
        test_cases = [
            {
                "content": "Compound interest is the interest calculated on the initial principal and the accumulated interest of previous periods.",
                "language": "Spanish",
                "user_level": "beginner"
            },
            {
                "content": "Diversification is a risk management strategy that mixes a wide variety of investments within a portfolio.",
                "language": "French",
                "user_level": "intermediate"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                result = await self.orchestrator.translation_agent.process(test_case)
                self.results.append({
                    "agent": "translation",
                    "test_case": i + 1,
                    "success": result.get("success", False),
                    "result": result
                })
                logger.info(f"Translation test {i + 1}: {'SUCCESS' if result.get('success') else 'FAILED'}")
            except Exception as e:
                logger.error(f"Translation test {i + 1} failed: {e}")
                self.results.append({
                    "agent": "translation",
                    "test_case": i + 1,
                    "success": False,
                    "error": str(e)
                })
    
    async def test_financial_planning_agent(self):
        """Test financial planning agent"""
        logger.info("Testing Financial Planning Agent...")
        
        test_cases = [
            {
                "goals": ["Buy a house in 5 years", "Save for retirement"],
                "income": 5000,
                "expenses": 3000,
                "timeline": "5 years"
            },
            {
                "goals": ["Emergency fund", "Pay off debt"],
                "income": 3000,
                "expenses": 2500,
                "timeline": "2 years"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                result = await self.orchestrator.financial_planning_agent.process(test_case)
                self.results.append({
                    "agent": "financial_planning",
                    "test_case": i + 1,
                    "success": result.get("success", False),
                    "result": result
                })
                logger.info(f"Financial planning test {i + 1}: {'SUCCESS' if result.get('success') else 'FAILED'}")
            except Exception as e:
                logger.error(f"Financial planning test {i + 1} failed: {e}")
                self.results.append({
                    "agent": "financial_planning",
                    "test_case": i + 1,
                    "success": False,
                    "error": str(e)
                })
    
    async def test_remittance_agent(self):
        """Test remittance agent"""
        logger.info("Testing Remittance Agent...")
        
        test_cases = [
            {
                "amount": 1000,
                "currency": "USD",
                "destination": "Mexico",
                "source_country": "USA",
                "destination_country": "Mexico"
            },
            {
                "amount": 500,
                "currency": "EUR",
                "destination": "India",
                "source_country": "Germany",
                "destination_country": "India"
            }
        ]
        
        for i, test_case in enumerate(test_cases):
            try:
                result = await self.orchestrator.remittance_agent.process(test_case)
                self.results.append({
                    "agent": "remittance",
                    "test_case": i + 1,
                    "success": result.get("success", False),
                    "result": result
                })
                logger.info(f"Remittance test {i + 1}: {'SUCCESS' if result.get('success') else 'FAILED'}")
            except Exception as e:
                logger.error(f"Remittance test {i + 1} failed: {e}")
                self.results.append({
                    "agent": "remittance",
                    "test_case": i + 1,
                    "success": False,
                    "error": str(e)
                })
    
    async def test_full_orchestration(self):
        """Test full orchestration workflow"""
        logger.info("Testing Full Orchestration...")
        
        test_request = {
            "goals": ["Save for education", "Build emergency fund"],
            "income": 4000,
            "expenses": 2500,
            "timeline": "3 years",
            "language": "English",
            "user_level": "intermediate"
        }
        
        try:
            result = await self.orchestrator.process_request(test_request)
            self.results.append({
                "agent": "orchestrator",
                "test_case": "full_workflow",
                "success": result.get("success", False),
                "result": result
            })
            logger.info(f"Full orchestration: {'SUCCESS' if result.get('success') else 'FAILED'}")
        except Exception as e:
            logger.error(f"Full orchestration failed: {e}")
            self.results.append({
                "agent": "orchestrator",
                "test_case": "full_workflow",
                "success": False,
                "error": str(e)
            })
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        total_tests = len(self.results)
        successful_tests = sum(1 for r in self.results if r.get("success", False))
        failed_tests = total_tests - successful_tests
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": failed_tests,
            "success_rate": f"{(successful_tests / total_tests * 100):.1f}%" if total_tests > 0 else "0%",
            "results": self.results
        }
        
        # Save report to file
        with open("demo/test_report.json", "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Test Report Generated:")
        logger.info(f"  Total Tests: {total_tests}")
        logger.info(f"  Successful: {successful_tests}")
        logger.info(f"  Failed: {failed_tests}")
        logger.info(f"  Success Rate: {report['success_rate']}")
        
        return report
    
    async def run_all_tests(self):
        """Run all agent tests"""
        logger.info("Starting Agent Demo Tests...")
        
        await self.test_translation_agent()
        await self.test_financial_planning_agent()
        await self.test_remittance_agent()
        await self.test_full_orchestration()
        
        report = self.generate_report()
        return report

async def main():
    """Main demo function"""
    demo = AgentDemo()
    report = await demo.run_all_tests()
    
    print("\n" + "="*50)
    print("REALITYCHECK AGENT DEMO COMPLETE")
    print("="*50)
    print(f"Total Tests: {report['total_tests']}")
    print(f"Successful: {report['successful_tests']}")
    print(f"Failed: {report['failed_tests']}")
    print(f"Success Rate: {report['success_rate']}")
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
