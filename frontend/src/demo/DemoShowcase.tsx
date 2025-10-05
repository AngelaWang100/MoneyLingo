import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  mockFinancialPlans, 
  mockVoiceResponses, 
  mockTranslations, 
  mockRemittanceAnalyses,
  mockUserProfile,
  mockDashboardData,
  type FinancialPlan,
  type VoiceResponse,
  type TranslationResult,
  type RemittanceAnalysis
} from './DemoData';

const DemoShowcase: React.FC = () => {
  const [selectedPlan, setSelectedPlan] = useState<FinancialPlan>(mockFinancialPlans[0]);
  const [selectedVoice, setSelectedVoice] = useState<VoiceResponse>(mockVoiceResponses[0]);
  const [selectedTranslation, setSelectedTranslation] = useState<TranslationResult>(mockTranslations[0]);
  const [selectedRemittance, setSelectedRemittance] = useState<RemittanceAnalysis>(mockRemittanceAnalyses[0]);
  const [isPlaying, setIsPlaying] = useState(false);

  const playVoice = () => {
    setIsPlaying(true);
    // Simulate audio playback
    setTimeout(() => setIsPlaying(false), selectedVoice.duration * 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚀 MoneyLingo Frontend Demo
          </h1>
          <p className="text-xl text-gray-600 mb-2">
            AI-Powered Financial Assistant with Voice & Translation
          </p>
          <Badge variant="outline" className="text-sm">
            Frontend Showcase - Mock Data Demo
          </Badge>
        </div>

        {/* Main Demo Tabs */}
        <Tabs defaultValue="dashboard" className="w-full">
          <TabsList className="grid w-full grid-cols-5">
            <TabsTrigger value="dashboard">Dashboard</TabsTrigger>
            <TabsTrigger value="financial">Financial Planning</TabsTrigger>
            <TabsTrigger value="voice">Voice AI</TabsTrigger>
            <TabsTrigger value="translation">Translation</TabsTrigger>
            <TabsTrigger value="remittance">Remittance</TabsTrigger>
          </TabsList>

          {/* Dashboard Tab */}
          <TabsContent value="dashboard" className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Total Assets</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">${mockDashboardData.totalAssets.toLocaleString()}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Monthly Income</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">${mockDashboardData.monthlyIncome.toLocaleString()}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Monthly Expenses</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-red-600">${mockDashboardData.monthlyExpenses.toLocaleString()}</div>
                </CardContent>
              </Card>
              
              <Card>
                <CardHeader className="pb-2">
                  <CardTitle className="text-sm font-medium">Savings Rate</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-blue-600">{(mockDashboardData.savingsRate * 100).toFixed(1)}%</div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Recent Transactions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockDashboardData.recentTransactions.map((transaction, index) => (
                    <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                      <div>
                        <div className="font-medium">{transaction.description}</div>
                        <div className="text-sm text-gray-500">{transaction.date}</div>
                      </div>
                      <div className={`font-bold ${transaction.amount > 0 ? 'text-green-600' : 'text-red-600'}`}>
                        {transaction.amount > 0 ? '+' : ''}${transaction.amount.toLocaleString()}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Financial Planning Tab */}
          <TabsContent value="financial" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Financial Plans</CardTitle>
                  <CardDescription>Select a plan to view details</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {mockFinancialPlans.map((plan) => (
                    <div 
                      key={plan.id}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedPlan.id === plan.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedPlan(plan)}
                    >
                      <div className="font-medium">{plan.goals.join(', ')}</div>
                      <div className="text-sm text-gray-500">Timeline: {plan.timeline}</div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Plan Details</CardTitle>
                  <CardDescription>{selectedPlan.timeline} timeline</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Goals:</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedPlan.goals.map((goal, index) => (
                        <Badge key={index} variant="secondary">{goal}</Badge>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <h4 className="font-medium mb-2">Recommendations:</h4>
                    <p className="text-sm text-gray-600">{selectedPlan.recommendations}</p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium mb-2">Risk Assessment:</h4>
                    <p className="text-sm text-gray-600">{selectedPlan.riskAssessment}</p>
                  </div>
                </CardContent>
              </Card>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>Milestones Progress</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {selectedPlan.milestones.map((milestone, index) => (
                    <div key={index} className="space-y-2">
                      <div className="flex justify-between">
                        <span className="font-medium">{milestone.description}</span>
                        <span className="text-sm text-gray-500">Month {milestone.month}</span>
                      </div>
                      <Progress value={Math.min((index + 1) * 25, 100)} className="h-2" />
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          {/* Voice AI Tab */}
          <TabsContent value="voice" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Voice Responses</CardTitle>
                  <CardDescription>Select a voice response to play</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {mockVoiceResponses.map((voice, index) => (
                    <div 
                      key={index}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedVoice === voice ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedVoice(voice)}
                    >
                      <div className="font-medium mb-2">{voice.text}</div>
                      <div className="flex justify-between text-sm text-gray-500">
                        <span>Language: {voice.language}</span>
                        <span>Duration: {voice.duration}s</span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Voice Player</CardTitle>
                  <CardDescription>Simulated voice playback</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <div className="font-medium mb-2">Selected Text:</div>
                    <p className="text-sm text-gray-600 mb-4">{selectedVoice.text}</p>
                    
                    <div className="flex items-center space-x-4">
                      <Button 
                        onClick={playVoice}
                        disabled={isPlaying}
                        className="flex items-center space-x-2"
                      >
                        {isPlaying ? (
                          <>
                            <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                            <span>Playing...</span>
                          </>
                        ) : (
                          <>
                            <div className="w-4 h-4 bg-white rounded-sm" />
                            <span>Play Voice</span>
                          </>
                        )}
                      </Button>
                      
                      <div className="text-sm text-gray-500">
                        Duration: {selectedVoice.duration}s
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Translation Tab */}
          <TabsContent value="translation" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Translation Examples</CardTitle>
                  <CardDescription>Select a translation to view</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {mockTranslations.map((translation, index) => (
                    <div 
                      key={index}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedTranslation === translation ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedTranslation(translation)}
                    >
                      <div className="font-medium mb-2">{translation.original}</div>
                      <div className="flex justify-between text-sm text-gray-500">
                        <span>Language: {translation.language}</span>
                        <span>Confidence: {(translation.confidence * 100).toFixed(1)}%</span>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Translation Result</CardTitle>
                  <CardDescription>AI-powered financial translation</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <h4 className="font-medium mb-2">Original:</h4>
                    <p className="text-sm text-gray-600 p-3 bg-gray-50 rounded">
                      {selectedTranslation.original}
                    </p>
                  </div>
                  
                  <div>
                    <h4 className="font-medium mb-2">Translated ({selectedTranslation.language}):</h4>
                    <p className="text-sm text-gray-600 p-3 bg-blue-50 rounded">
                      {selectedTranslation.translated}
                    </p>
                  </div>
                  
                  <div className="flex justify-between text-sm">
                    <span>Confidence: {(selectedTranslation.confidence * 100).toFixed(1)}%</span>
                    <Badge variant="outline">{selectedTranslation.language.toUpperCase()}</Badge>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          {/* Remittance Tab */}
          <TabsContent value="remittance" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Remittance Analysis</CardTitle>
                  <CardDescription>Select a remittance scenario</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {mockRemittanceAnalyses.map((analysis, index) => (
                    <div 
                      key={index}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedRemittance === analysis ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedRemittance(analysis)}
                    >
                      <div className="font-medium mb-2">
                        ${analysis.amount} {analysis.fromCountry} → {analysis.toCountry}
                      </div>
                      <div className="text-sm text-gray-500">
                        Best: {analysis.bestMethod} | Fees: ${analysis.estimatedFees}
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Analysis Details</CardTitle>
                  <CardDescription>AI-powered remittance optimization</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <div className="text-sm text-gray-500">Amount</div>
                      <div className="font-bold">${selectedRemittance.amount.toLocaleString()}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Route</div>
                      <div className="font-bold">{selectedRemittance.fromCountry} → {selectedRemittance.toCountry}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Best Method</div>
                      <div className="font-bold">{selectedRemittance.bestMethod}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Fees</div>
                      <div className="font-bold">${selectedRemittance.estimatedFees}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Exchange Rate</div>
                      <div className="font-bold">{selectedRemittance.exchangeRate}</div>
                    </div>
                    <div>
                      <div className="text-sm text-gray-500">Total Cost</div>
                      <div className="font-bold">${selectedRemittance.totalCost}</div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>

        {/* Footer */}
        <div className="mt-12 text-center">
          <Card>
            <CardContent className="pt-6">
              <div className="space-y-4">
                <h3 className="text-lg font-semibold">🎯 Frontend Demo Features</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <div className="font-medium">✅ Responsive Design</div>
                    <div className="text-gray-600">Mobile-first, modern UI</div>
                  </div>
                  <div>
                    <div className="font-medium">✅ Interactive Components</div>
                    <div className="text-gray-600">Real-time data visualization</div>
                  </div>
                  <div>
                    <div className="font-medium">✅ Mock Data Integration</div>
                    <div className="text-gray-600">Realistic demo scenarios</div>
                  </div>
                </div>
                <div className="text-sm text-gray-500">
                  This frontend demonstrates the complete user interface and user experience 
                  that would connect to the backend APIs when fully integrated.
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DemoShowcase;
