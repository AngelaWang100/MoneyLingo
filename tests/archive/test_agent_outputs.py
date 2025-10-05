#!/usr/bin/env python3
"""
Test RealityCheck agents and show detailed outputs
"""
import asyncio
import os
import json
from dotenv import load_dotenv
from agents.translation_agent import TranslationAgent
from agents.financial_planning_agent import FinancialPlanningAgent
from agents.remittance_agent import RemittanceAgent

# Load environment variables
load_dotenv()

async def test_translation_agent_detailed():
    """Test Translation Agent with detailed output"""
    print("🌍 TRANSLATION AGENT TEST")
    print("=" * 50)
    
    agent = TranslationAgent()
    test_data = {
        "content": "Diversification is a risk management strategy that mixes a wide variety of investments within a portfolio.",
        "language": "Spanish",
        "user_level": "beginner"
    }
    
    print(f"📝 Input: {test_data['content']}")
    print(f"🌍 Target Language: {test_data['language']}")
    print(f"👤 User Level: {test_data['user_level']}")
    print()
    
    result = await agent.process(test_data)
    
    if result.get("success"):
        print("✅ SUCCESS!")
        print(f"📄 Translated Content:")
        print("-" * 30)
        print(result.get('translated_content', 'No content'))
        print("-" * 30)
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result

async def test_financial_planning_agent_detailed():
    """Test Financial Planning Agent with detailed output"""
    print("\n💰 FINANCIAL PLANNING AGENT TEST")
    print("=" * 50)
    
    agent = FinancialPlanningAgent()
    test_data = {
        "goals": ["Save for retirement", "Buy a house in 5 years"],
        "income": 5000,
        "expenses": 3000,
        "timeline": "5 years"
    }
    
    print(f"🎯 Goals: {test_data['goals']}")
    print(f"💵 Income: ${test_data['income']}")
    print(f"💸 Expenses: ${test_data['expenses']}")
    print(f"⏰ Timeline: {test_data['timeline']}")
    print()
    
    result = await agent.process(test_data)
    
    if result.get("success"):
        print("✅ SUCCESS!")
        print(f"📄 AI Recommendations:")
        print("-" * 30)
        print(result.get('ai_recommendations', 'No recommendations'))
        print("-" * 30)
        print(f"🔌 Backend Plan: {result.get('backend_plan', {})}")
        print(f"💳 Transaction Insights: {result.get('transaction_insights', {})}")
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result

async def test_remittance_agent_detailed():
    """Test Remittance Agent with detailed output"""
    print("\n💸 REMITTANCE AGENT TEST")
    print("=" * 50)
    
    agent = RemittanceAgent()
    test_data = {
        "amount": 1000,
        "currency": "USD",
        "destination": "Mexico",
        "source_country": "USA",
        "destination_country": "Mexico"
    }
    
    print(f"💰 Amount: {test_data['amount']} {test_data['currency']}")
    print(f"🌍 From: {test_data['source_country']}")
    print(f"🌍 To: {test_data['destination_country']}")
    print(f"📍 Destination: {test_data['destination']}")
    print()
    
    result = await agent.process(test_data)
    
    if result.get("success"):
        print("✅ SUCCESS!")
        print(f"📄 AI Analysis:")
        print("-" * 30)
        print(result.get('ai_analysis', 'No analysis'))
        print("-" * 30)
        print(f"🔌 Remittance Data: {result.get('remittance_data', {})}")
    else:
        print("❌ FAILED!")
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result

async def main():
    print("🧪 REALITYCHECK AGENT OUTPUT ANALYSIS")
    print("=" * 60)
    print("Testing all agents with detailed output inspection...")
    print()
    
    # Test all agents
    translation_result = await test_translation_agent_detailed()
    financial_result = await test_financial_planning_agent_detailed()
    remittance_result = await test_remittance_agent_detailed()
    
    # Summary
    print("\n📊 SUMMARY")
    print("=" * 60)
    print(f"🌍 Translation Agent: {'✅ SUCCESS' if translation_result.get('success') else '❌ FAILED'}")
    print(f"💰 Financial Planning Agent: {'✅ SUCCESS' if financial_result.get('success') else '❌ FAILED'}")
    print(f"💸 Remittance Agent: {'✅ SUCCESS' if remittance_result.get('success') else '❌ FAILED'}")
    
    # Save results to file
    results = {
        "translation": translation_result,
        "financial_planning": financial_result,
        "remittance": remittance_result
    }
    
    with open("agent_outputs.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: agent_outputs.json")
    print("🎉 Agent output analysis complete!")

if __name__ == "__main__":
    asyncio.run(main())
