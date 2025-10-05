/**
 * Demo Data for Frontend Showcase
 * Mock data to demonstrate frontend functionality without backend integration
 */

export interface FinancialPlan {
  id: string;
  goals: string[];
  income: number;
  expenses: number;
  timeline: string;
  recommendations: string;
  riskAssessment: string;
  milestones: Array<{
    month: number;
    target: number;
    description: string;
  }>;
}

export interface VoiceResponse {
  text: string;
  audioUrl: string;
  language: string;
  duration: number;
}

export interface TranslationResult {
  original: string;
  translated: string;
  language: string;
  confidence: number;
}

export interface RemittanceAnalysis {
  amount: number;
  fromCountry: string;
  toCountry: string;
  bestMethod: string;
  estimatedFees: number;
  exchangeRate: number;
  totalCost: number;
}

export const mockFinancialPlans: FinancialPlan[] = [
  {
    id: "plan_001",
    goals: ["Retirement savings", "Emergency fund", "Home purchase"],
    income: 7500,
    expenses: 4500,
    timeline: "5 years",
    recommendations: "Based on your income and expenses, you should save $1,500 monthly. Allocate 60% to retirement (401k/IRA), 30% to emergency fund, and 10% to home down payment. Consider index funds for long-term growth.",
    riskAssessment: "Moderate risk tolerance suitable for balanced portfolio",
    milestones: [
      { month: 6, target: 9000, description: "Emergency fund (3 months expenses)" },
      { month: 18, target: 27000, description: "Emergency fund (6 months expenses)" },
      { month: 36, target: 54000, description: "Home down payment (20%)" },
      { month: 60, target: 90000, description: "Retirement fund milestone" }
    ]
  },
  {
    id: "plan_002", 
    goals: ["Debt payoff", "Investment portfolio", "Travel fund"],
    income: 6000,
    expenses: 4000,
    timeline: "3 years",
    recommendations: "Focus on debt elimination first. Pay extra $500 monthly on high-interest debt. Once debt-free, invest $1,000 monthly in diversified ETFs. Set aside $200 monthly for travel.",
    riskAssessment: "Conservative approach with gradual risk increase",
    milestones: [
      { month: 12, target: 12000, description: "Credit card debt eliminated" },
      { month: 24, target: 24000, description: "Student loan payoff" },
      { month: 36, target: 36000, description: "Investment portfolio established" }
    ]
  }
];

export const mockVoiceResponses: VoiceResponse[] = [
  {
    text: "Welcome to MoneyLingo! Your AI financial assistant is ready to help you plan for the future.",
    audioUrl: "/demo-audio/welcome.mp3",
    language: "en",
    duration: 4.2
  },
  {
    text: "Based on your financial profile, I recommend starting with an emergency fund of 3-6 months expenses.",
    audioUrl: "/demo-audio/emergency-fund.mp3", 
    language: "en",
    duration: 6.1
  },
  {
    text: "Bienvenido a MoneyLingo! Su asistente financiero de IA está listo para ayudarle a planificar el futuro.",
    audioUrl: "/demo-audio/welcome-es.mp3",
    language: "es", 
    duration: 4.8
  }
];

export const mockTranslations: TranslationResult[] = [
  {
    original: "Your monthly budget should include 50% for needs, 30% for wants, and 20% for savings.",
    translated: "Su presupuesto mensual debe incluir 50% para necesidades, 30% para deseos y 20% para ahorros.",
    language: "es",
    confidence: 0.95
  },
  {
    original: "Diversify your investment portfolio to reduce risk.",
    translated: "Diversifiez votre portefeuille d'investissement pour réduire les risques.",
    language: "fr",
    confidence: 0.92
  },
  {
    original: "Start investing early to benefit from compound interest.",
    translated: "Comience a invertir temprano para beneficiarse del interés compuesto.",
    language: "es",
    confidence: 0.94
  }
];

export const mockRemittanceAnalyses: RemittanceAnalysis[] = [
  {
    amount: 1000,
    fromCountry: "US",
    toCountry: "Mexico", 
    bestMethod: "Wise (formerly TransferWise)",
    estimatedFees: 4.50,
    exchangeRate: 17.85,
    totalCost: 1004.50
  },
  {
    amount: 500,
    fromCountry: "US",
    toCountry: "India",
    bestMethod: "Remitly",
    estimatedFees: 2.99,
    exchangeRate: 83.25,
    totalCost: 502.99
  },
  {
    amount: 2000,
    fromCountry: "US", 
    toCountry: "Philippines",
    bestMethod: "Wise",
    estimatedFees: 8.25,
    exchangeRate: 56.75,
    totalCost: 2008.25
  }
];

export const mockUserProfile = {
  name: "Demo User",
  email: "demo@moneylingo.com",
  preferredLanguage: "en",
  riskTolerance: "moderate",
  financialGoals: ["Retirement", "Emergency Fund", "Home Purchase"],
  monthlyIncome: 7500,
  monthlyExpenses: 4500,
  currentSavings: 15000
};

export const mockDashboardData = {
  totalAssets: 15000,
  monthlyIncome: 7500,
  monthlyExpenses: 4500,
  netWorth: 15000,
  savingsRate: 0.4,
  debtToIncome: 0.15,
  creditScore: 780,
  recentTransactions: [
    { date: "2024-01-15", description: "Salary", amount: 7500, type: "income" },
    { date: "2024-01-14", description: "Rent", amount: -2000, type: "expense" },
    { date: "2024-01-13", description: "Groceries", amount: -300, type: "expense" },
    { date: "2024-01-12", description: "Investment", amount: -1000, type: "savings" }
  ]
};
