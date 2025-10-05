import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { Link } from "react-router-dom";
import { MessageSquare, FileText, TrendingUp, Clock, CheckCircle2, Lock, ExternalLink, BookOpen, Video, FileCheck, PiggyBank, CreditCard, Calculator, Target, DollarSign, BarChart3, PieChart, Wallet, Shield } from "lucide-react";
import { useState, useEffect } from "react";
import { useToast } from "@/hooks/use-toast";
import { apiClient } from "@/lib/api";

const Dashboard = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [financialPlan, setFinancialPlan] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  // Financial planning form state
  const [planForm, setPlanForm] = useState({
    income: "",
    expenses: "",
    goals: [] as string[],
    timeline: "1 year",
    language: "en",
    userLevel: "beginner"
  });

  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(authStatus);
  }, []);

  const handleCreateFinancialPlan = async () => {
    if (!planForm.income || !planForm.expenses) {
      toast({
        title: "Missing Information",
        description: "Please fill in your income and expenses.",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiClient.getFinancialAdvice({
        question: `Create a financial plan for someone with $${planForm.income} income and $${planForm.expenses} expenses, goals: ${planForm.goals.join(", ")}, timeline: ${planForm.timeline}`,
        user_level: planForm.userLevel as any,
        language: planForm.language
      });

      if (response.success) {
        setFinancialPlan(response.data);
        toast({
          title: "Financial Plan Created!",
          description: "Your personalized financial plan is ready.",
        });
      }
    } catch (error) {
      console.error('Financial planning error:', error);
      toast({
        title: "Error",
        description: "Failed to create financial plan. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const goalDetails = {
    "Build Credit Score": {
      title: "Build Credit Score",
      target: "Target: 700+ by June 2024",
      summary: "Building a strong credit score is essential for accessing better financial opportunities, including loans, mortgages, and credit cards with favorable terms.",
      steps: [
        "Pay all bills on time - payment history is 35% of your credit score",
        "Keep credit card balances below 30% of your limit",
        "Don't close old credit cards - length of credit history matters",
        "Only apply for new credit when necessary",
        "Monitor your credit report regularly for errors"
      ],
      resources: [
        { title: "Understanding Credit Scores Guide", type: "article", icon: BookOpen },
        { title: "Credit Building Video Tutorial", type: "video", icon: Video },
        { title: "Free Credit Report Access", type: "tool", icon: FileCheck }
      ]
    },
    "Understand Tax Forms": {
      title: "Understand Tax Forms",
      target: "Complete guide walkthrough",
      summary: "Understanding tax forms is crucial for filing your taxes correctly and taking advantage of all available deductions and credits.",
      steps: [
        "Learn about W-2 forms and how to read them",
        "Understand different types of 1099 forms",
        "Know which deductions you qualify for",
        "Learn about tax credits vs. tax deductions",
        "Understand filing status and its impact"
      ],
      resources: [
        { title: "Tax Forms Explained", type: "article", icon: BookOpen },
        { title: "Filing Taxes Step-by-Step", type: "video", icon: Video },
        { title: "Tax Calculator Tool", type: "tool", icon: FileCheck }
      ]
    }
  };

  const recentActivity = [
    { id: 1, type: "chat", title: "Asked about credit scores", time: "2 hours ago" },
    { id: 2, type: "document", title: "Uploaded tax return 2023", time: "1 day ago" },
    { id: 3, type: "plan", title: "Viewed credit building plan", time: "2 days ago" },
  ];

  const insights = [
    { title: "Credit Score Progress", value: "+15 points", change: "this month", positive: true },
    { title: "Documents Analyzed", value: "3", change: "total", positive: true },
    { title: "AI Sessions", value: "12", change: "this week", positive: true },
  ];

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Decorative Background */}
      <div className="fixed inset-0 bg-gradient-mesh opacity-40 pointer-events-none" />
      <div className="fixed top-20 right-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="fixed bottom-20 left-10 w-96 h-96 bg-accent/20 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <Header />

      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 relative z-10 animate-fade-in">
        <div className="mb-6 sm:mb-8 animate-scale-in px-4 sm:px-0">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold shimmer-text mb-2 leading-tight">
            {isAuthenticated ? 'Welcome Back!' : 'Dashboard Preview'}
          </h1>
          <p className="text-sm sm:text-base text-muted-foreground">
            {isAuthenticated ? "Here's your financial literacy progress." : 'Sign in to track your financial journey.'}
          </p>
        </div>

        {/* Auth Alert */}
        {!isAuthenticated && (
          <Alert className="mb-6 border-primary/50 bg-primary/5 glass-card animate-fade-in">
            <Lock className="h-4 w-4 text-primary" />
            <AlertDescription className="flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:justify-between">
              <span className="text-sm">Create an account to access your personalized dashboard and track your progress.</span>
              <div className="flex gap-2 w-full sm:w-auto ml-0 sm:ml-4">
                <Button size="sm" asChild className="flex-1 sm:flex-initial bg-gradient-primary hover:scale-105 transition-all duration-300 shadow-lg">
                  <Link to="/signin">Sign In</Link>
                </Button>
                <Button size="sm" variant="outline" asChild className="flex-1 sm:flex-initial hover-card-lift">
                  <Link to="/signup">Sign Up</Link>
                </Button>
              </div>
            </AlertDescription>
          </Alert>
        )}

        {/* Quick Actions */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4 mb-6 sm:mb-8 animate-fade-in-up">
          <Link to="/chat">
            <Card className="glass-card hover:border-primary/50 transition-all hover-card-lift cursor-pointer">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg">
                    <MessageSquare className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Start AI Chat</CardTitle>
                    <CardDescription className="text-sm">Ask financial questions</CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </Link>

          <Link to="/documents">
            <Card className="glass-card hover:border-primary/50 transition-all hover-card-lift cursor-pointer">
              <CardHeader>
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg">
                    <FileText className="h-6 w-6 text-primary-foreground" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Upload Document</CardTitle>
                    <CardDescription className="text-sm">Analyze financial files</CardDescription>
                  </div>
                </div>
              </CardHeader>
            </Card>
          </Link>
        </div>

        <div className="grid lg:grid-cols-3 gap-6 sm:gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
              <TabsList className="grid w-full grid-cols-4">
                <TabsTrigger value="overview">Overview</TabsTrigger>
                <TabsTrigger value="planning">Financial Planning</TabsTrigger>
                <TabsTrigger value="goals">Goals</TabsTrigger>
                <TabsTrigger value="analytics">Analytics</TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                {/* Insights */}
                <Card className="glass-card animate-fade-in-up">
                  <CardHeader>
                    <CardTitle className="text-xl">Your Progress</CardTitle>
                    <CardDescription>Key metrics from your financial journey</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-3 gap-4">
                      {insights.map((insight, index) => (
                        <div key={insight.title} className="p-4 rounded-xl bg-gradient-card border-2 border-border/50 hover-card-lift animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                          <p className="text-sm text-muted-foreground mb-1">{insight.title}</p>
                          <p className="text-2xl font-bold shimmer-text">{insight.value}</p>
                          <p className="text-xs text-muted-foreground">{insight.change}</p>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* Recent Activity */}
                <Card className="glass-card animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
                  <CardHeader>
                    <CardTitle>Recent Activity</CardTitle>
                    <CardDescription>Your latest interactions and progress</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {recentActivity.map((activity) => (
                        <Button
                          key={activity.id}
                          variant="ghost"
                          className="w-full h-auto p-4 justify-start hover-lift border border-border/50 hover:border-primary/30 hover:bg-accent/5"
                          asChild
                        >
                          <Link to={activity.type === "chat" ? "/chat" : activity.type === "document" ? "/documents" : "/dashboard"}>
                            <div className="flex items-start gap-4 w-full">
                              <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                                {activity.type === "chat" && <MessageSquare className="h-5 w-5 text-primary" />}
                                {activity.type === "document" && <FileText className="h-5 w-5 text-accent" />}
                                {activity.type === "plan" && <TrendingUp className="h-5 w-5 text-primary" />}
                              </div>
                              <div className="flex-1 min-w-0 text-left">
                                <p className="font-medium text-foreground truncate">{activity.title}</p>
                                <p className="text-sm text-muted-foreground flex items-center gap-1">
                                  <Clock className="h-3 w-3" />
                                  {activity.time}
                                </p>
                              </div>
                              <ExternalLink className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                            </div>
                          </Link>
                        </Button>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="planning" className="space-y-6">
                {/* Financial Planning Form */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Create Your Financial Plan
                    </CardTitle>
                    <CardDescription>
                      Get personalized financial advice based on your situation
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="income">Monthly Income</Label>
                        <Input
                          id="income"
                          type="number"
                          placeholder="5000"
                          value={planForm.income}
                          onChange={(e) => setPlanForm(prev => ({ ...prev, income: e.target.value }))}
                        />
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="expenses">Monthly Expenses</Label>
                        <Input
                          id="expenses"
                          type="number"
                          placeholder="3000"
                          value={planForm.expenses}
                          onChange={(e) => setPlanForm(prev => ({ ...prev, expenses: e.target.value }))}
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-4">
                      <div className="space-y-2">
                        <Label htmlFor="timeline">Timeline</Label>
                        <Select value={planForm.timeline} onValueChange={(value) => setPlanForm(prev => ({ ...prev, timeline: value }))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="6 months">6 months</SelectItem>
                            <SelectItem value="1 year">1 year</SelectItem>
                            <SelectItem value="2 years">2 years</SelectItem>
                            <SelectItem value="5 years">5 years</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                      <div className="space-y-2">
                        <Label htmlFor="level">Experience Level</Label>
                        <Select value={planForm.userLevel} onValueChange={(value) => setPlanForm(prev => ({ ...prev, userLevel: value }))}>
                          <SelectTrigger>
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="beginner">Beginner</SelectItem>
                            <SelectItem value="intermediate">Intermediate</SelectItem>
                            <SelectItem value="advanced">Advanced</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>

                    <Button 
                      onClick={handleCreateFinancialPlan} 
                      disabled={isLoading}
                      className="w-full"
                    >
                      {isLoading ? "Creating Plan..." : "Create Financial Plan"}
                    </Button>
                  </CardContent>
                </Card>

                {/* Financial Plan Results */}
                {financialPlan && (
                  <Card className="glass-card">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <PiggyBank className="h-5 w-5" />
                        Your Financial Plan
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="p-4 bg-muted rounded-lg">
                          <h4 className="font-semibold mb-2">AI Recommendations</h4>
                          <p className="text-sm">{financialPlan.advice}</p>
                        </div>
                        
                        {financialPlan.recommendations && (
                          <div className="space-y-2">
                            <h4 className="font-semibold">Key Recommendations</h4>
                            <ul className="space-y-1">
                              {financialPlan.recommendations.map((rec: string, index: number) => (
                                <li key={index} className="flex items-start gap-2 text-sm">
                                  <CheckCircle2 className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                                  {rec}
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}

                        <div className="flex items-center gap-2 p-3 bg-primary/10 rounded-lg">
                          <Shield className="h-4 w-4 text-primary" />
                          <span className="text-sm font-medium">Risk Level: {financialPlan.risk_level}</span>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="goals" className="space-y-6">
                {/* Financial Goals */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Target className="h-5 w-5" />
                      Financial Goals
                    </CardTitle>
                    <CardDescription>
                      Track your financial objectives and progress
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {Object.entries(goalDetails).map(([goalKey, goal]) => (
                        <Card key={goalKey} className="cursor-pointer hover:shadow-md transition-all" onClick={() => setSelectedGoal(goalKey)}>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div>
                                <h3 className="font-semibold">{goal.title}</h3>
                                <p className="text-sm text-muted-foreground">{goal.target}</p>
                              </div>
                              <Progress value={Math.random() * 100} className="w-24" />
                            </div>
                          </CardContent>
                        </Card>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="analytics" className="space-y-6">
                {/* Financial Analytics */}
                <div className="grid md:grid-cols-2 gap-6">
                  <Card className="glass-card">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <BarChart3 className="h-5 w-5" />
                        Spending Analysis
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Housing</span>
                          <Badge variant="secondary">40%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Food</span>
                          <Badge variant="secondary">25%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Transportation</span>
                          <Badge variant="secondary">15%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Entertainment</span>
                          <Badge variant="secondary">10%</Badge>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-sm">Savings</span>
                          <Badge variant="secondary">10%</Badge>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="glass-card">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <PieChart className="h-5 w-5" />
                        Net Worth
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center space-y-4">
                        <div className="text-3xl font-bold shimmer-text">$45,230</div>
                        <div className="text-sm text-muted-foreground">+12% from last month</div>
                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span>Assets</span>
                            <span className="text-green-600">$52,000</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Liabilities</span>
                            <span className="text-red-600">$6,770</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Current Goals */}
            <Card className="glass-card animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
              <CardHeader>
                <CardTitle className="text-xl">Current Goals</CardTitle>
                <CardDescription>Your active financial objectives</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <Button
                  variant="ghost"
                  className="w-full h-auto p-4 justify-start hover-lift border border-border/50 hover:border-primary/30 hover:bg-accent/5"
                  onClick={() => setSelectedGoal("Build Credit Score")}
                >
                  <div className="flex items-start gap-3 w-full">
                    <CheckCircle2 className="h-5 w-5 text-primary flex-shrink-0 mt-0.5" />
                    <div className="flex-1 text-left">
                      <p className="font-medium mb-1">Build Credit Score</p>
                      <p className="text-sm text-muted-foreground">Target: 700+ by June 2024</p>
                    </div>
                    <ExternalLink className="h-4 w-4 text-muted-foreground flex-shrink-0 mt-1" />
                  </div>
                </Button>

                <Button
                  variant="ghost"
                  className="w-full h-auto p-4 justify-start hover-lift border border-border/50 hover:border-primary/30 hover:bg-accent/5"
                  onClick={() => setSelectedGoal("Understand Tax Forms")}
                >
                  <div className="flex items-start gap-3 w-full">
                    <CheckCircle2 className="h-5 w-5 text-muted-foreground flex-shrink-0 mt-0.5" />
                    <div className="flex-1 text-left">
                      <p className="font-medium mb-1">Understand Tax Forms</p>
                      <p className="text-sm text-muted-foreground">Complete guide walkthrough</p>
                    </div>
                    <ExternalLink className="h-4 w-4 text-muted-foreground flex-shrink-0 mt-1" />
                  </div>
                </Button>

                <Button variant="outline" className="w-full hover-card-lift bg-gradient-primary text-primary-foreground hover:scale-105 transition-all duration-300 shadow-lg" disabled={!isAuthenticated}>Add New Goal</Button>
              </CardContent>
            </Card>

            {/* Help Resources */}
            <Card className="glass-card animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
              <CardHeader>
                <CardTitle className="text-xl">Need Help?</CardTitle>
                <CardDescription>Access resources and support</CardDescription>
              </CardHeader>
              <CardContent className="space-y-2">
                <Button variant="ghost" className="w-full justify-start hover-lift" asChild>
                  <Link to="/#faq">
                    FAQ
                  </Link>
                </Button>
                <Button variant="ghost" className="w-full justify-start hover-lift" asChild>
                  <Link to="/chat">
                    Ask AI Assistant
                  </Link>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />

      {/* Goal Details Dialog */}
      <Dialog open={!!selectedGoal} onOpenChange={() => setSelectedGoal(null)}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto glass-card">
          {selectedGoal && goalDetails[selectedGoal as keyof typeof goalDetails] && (
            <>
              <DialogHeader>
                <DialogTitle className="text-2xl shimmer-text">
                  {goalDetails[selectedGoal as keyof typeof goalDetails].title}
                </DialogTitle>
                <DialogDescription className="text-base">
                  {goalDetails[selectedGoal as keyof typeof goalDetails].target}
                </DialogDescription>
              </DialogHeader>

              <div className="space-y-6 mt-4">
                {/* Summary */}
                <div>
                  <h3 className="font-semibold text-lg mb-2">Overview</h3>
                  <p className="text-muted-foreground">
                    {goalDetails[selectedGoal as keyof typeof goalDetails].summary}
                  </p>
                </div>

                {/* Action Steps */}
                <div>
                  <h3 className="font-semibold text-lg mb-3">Action Steps</h3>
                  <div className="space-y-3">
                    {goalDetails[selectedGoal as keyof typeof goalDetails].steps.map((step, index) => (
                      <div key={index} className="flex items-start gap-3 p-3 rounded-lg bg-muted/50">
                        <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                          <span className="text-sm font-semibold text-primary">{index + 1}</span>
                        </div>
                        <p className="text-sm">{step}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Resources */}
                <div>
                  <h3 className="font-semibold text-lg mb-3">Helpful Resources</h3>
                  <div className="space-y-2">
                    {goalDetails[selectedGoal as keyof typeof goalDetails].resources.map((resource, index) => (
                      <Button
                        key={index}
                        variant="outline"
                        className="w-full justify-start hover-lift"
                      >
                        <resource.icon className="h-4 w-4 text-primary mr-2" />
                        <span className="flex-1 text-left">{resource.title}</span>
                        <span className="text-xs text-muted-foreground px-2 py-1 bg-muted rounded">
                          {resource.type}
                        </span>
                      </Button>
                    ))}
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3 pt-4 border-t">
                  <Button className="flex-1 bg-gradient-primary hover:scale-105 transition-all duration-300 shadow-lg" asChild>
                    <Link to="/chat">Ask AI Assistant</Link>
                  </Button>
                  <Button variant="outline" className="flex-1 hover-card-lift" onClick={() => setSelectedGoal(null)}>
                    Close
                  </Button>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Dashboard;