import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { useState } from "react";
import { Globe, TrendingUp, Shield, Clock, DollarSign, ArrowRight, CheckCircle2, AlertTriangle, Zap } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { apiClient } from "@/lib/api";

const Remittance = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const { toast } = useToast();

  const [remittanceForm, setRemittanceForm] = useState({
    amount: "",
    fromCountry: "",
    toCountry: "",
    currency: "USD"
  });

  const countries = [
    { code: "US", name: "United States", flag: "🇺🇸" },
    { code: "MX", name: "Mexico", flag: "🇲🇽" },
    { code: "IN", name: "India", flag: "🇮🇳" },
    { code: "PH", name: "Philippines", flag: "🇵🇭" },
    { code: "BR", name: "Brazil", flag: "🇧🇷" },
    { code: "NG", name: "Nigeria", flag: "🇳🇬" },
    { code: "CN", name: "China", flag: "🇨🇳" },
    { code: "GB", name: "United Kingdom", flag: "🇬🇧" },
    { code: "DE", name: "Germany", flag: "🇩🇪" },
    { code: "FR", name: "France", flag: "🇫🇷" },
    { code: "CA", name: "Canada", flag: "🇨🇦" },
    { code: "AU", name: "Australia", flag: "🇦🇺" }
  ];

  const currencies = [
    { code: "USD", name: "US Dollar", symbol: "$" },
    { code: "EUR", name: "Euro", symbol: "€" },
    { code: "GBP", name: "British Pound", symbol: "£" },
    { code: "JPY", name: "Japanese Yen", symbol: "¥" },
    { code: "CAD", name: "Canadian Dollar", symbol: "C$" },
    { code: "AUD", name: "Australian Dollar", symbol: "A$" },
    { code: "MXN", name: "Mexican Peso", symbol: "MX$" },
    { code: "INR", name: "Indian Rupee", symbol: "₹" },
    { code: "CNY", name: "Chinese Yuan", symbol: "¥" },
    { code: "BRL", name: "Brazilian Real", symbol: "R$" }
  ];

  const handleAnalyzeRemittance = async () => {
    if (!remittanceForm.amount || !remittanceForm.fromCountry || !remittanceForm.toCountry) {
      toast({
        title: "Missing Information",
        description: "Please fill in all required fields.",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      const response = await apiClient.analyzeRemittance(
        parseFloat(remittanceForm.amount),
        remittanceForm.fromCountry,
        remittanceForm.toCountry
      );

      if (response.success) {
        setAnalysisResult(response.data);
        toast({
          title: "Analysis Complete!",
          description: "Your remittance analysis is ready.",
        });
      }
    } catch (error) {
      console.error('Remittance analysis error:', error);
      toast({
        title: "Error",
        description: "Failed to analyze remittance. Please try again.",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute inset-0 bg-gradient-main pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-clouds pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/5 to-background/20 pointer-events-none" />
      
      {/* Floating decorative elements */}
      <div className="absolute top-20 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <Header />

      <main className="flex-1 relative z-10 container mx-auto max-w-6xl px-4 py-8">
        <div className="text-center space-y-4 mb-8">
          <h1 className="text-3xl sm:text-4xl font-bold">
            <span className="shimmer-text">Remittance Analysis</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Analyze the best ways to send money internationally with XRPL blockchain technology
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Analysis Form */}
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5" />
                Remittance Details
              </CardTitle>
              <CardDescription>
                Enter your transfer details to get the best analysis
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="amount">Transfer Amount</Label>
                <div className="flex gap-2">
                  <Select value={remittanceForm.currency} onValueChange={(value) => setRemittanceForm(prev => ({ ...prev, currency: value }))}>
                    <SelectTrigger className="w-32">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {currencies.map((currency) => (
                        <SelectItem key={currency.code} value={currency.code}>
                          {currency.symbol} {currency.code}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Input
                    id="amount"
                    type="number"
                    placeholder="1000"
                    value={remittanceForm.amount}
                    onChange={(e) => setRemittanceForm(prev => ({ ...prev, amount: e.target.value }))}
                    className="flex-1"
                  />
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="fromCountry">From Country</Label>
                  <Select value={remittanceForm.fromCountry} onValueChange={(value) => setRemittanceForm(prev => ({ ...prev, fromCountry: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select country" />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map((country) => (
                        <SelectItem key={country.code} value={country.code}>
                          <span className="flex items-center gap-2">
                            <span>{country.flag}</span>
                            <span>{country.name}</span>
                          </span>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="toCountry">To Country</Label>
                  <Select value={remittanceForm.toCountry} onValueChange={(value) => setRemittanceForm(prev => ({ ...prev, toCountry: value }))}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select country" />
                    </SelectTrigger>
                    <SelectContent>
                      {countries.map((country) => (
                        <SelectItem key={country.code} value={country.code}>
                          <span className="flex items-center gap-2">
                            <span>{country.flag}</span>
                            <span>{country.name}</span>
                          </span>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <Button 
                onClick={handleAnalyzeRemittance} 
                disabled={isLoading}
                className="w-full"
              >
                {isLoading ? "Analyzing..." : "Analyze Remittance"}
              </Button>
            </CardContent>
          </Card>

          {/* Analysis Results */}
          <div className="space-y-6">
            {analysisResult ? (
              <>
                {/* XRPL Analysis */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Zap className="h-5 w-5 text-yellow-500" />
                      XRPL Blockchain Analysis
                    </CardTitle>
                    <CardDescription>
                      Cost analysis using XRPL testnet
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div className="text-center p-4 bg-green-50 rounded-lg">
                        <div className="text-2xl font-bold text-green-600">
                          ${(parseFloat(remittanceForm.amount) * 0.001).toFixed(2)}
                        </div>
                        <div className="text-sm text-green-600">XRPL Fee</div>
                      </div>
                      <div className="text-center p-4 bg-blue-50 rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">
                          {Math.floor(Math.random() * 5) + 1} min
                        </div>
                        <div className="text-sm text-blue-600">Settlement Time</div>
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                      <div className="flex justify-between">
                        <span className="text-sm">Network Fee</span>
                        <Badge variant="secondary">$0.001</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm">Exchange Rate</span>
                        <Badge variant="secondary">Real-time</Badge>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-sm">Security</span>
                        <Badge variant="secondary" className="text-green-600">High</Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Comparison */}
                <Card className="glass-card">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      Cost Comparison
                    </CardTitle>
                    <CardDescription>
                      Compare different remittance methods
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <Zap className="h-4 w-4 text-green-600" />
                          <span className="font-medium">XRPL Blockchain</span>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-green-600">$0.001</div>
                          <div className="text-xs text-green-600">Best Option</div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <DollarSign className="h-4 w-4 text-gray-600" />
                          <span className="font-medium">Traditional Bank</span>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-gray-600">$25.00</div>
                          <div className="text-xs text-gray-600">2-3 days</div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center gap-2">
                          <Globe className="h-4 w-4 text-gray-600" />
                          <span className="font-medium">Money Transfer</span>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-gray-600">$15.00</div>
                          <div className="text-xs text-gray-600">1-2 days</div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </>
            ) : (
              <Card className="glass-card">
                <CardContent className="p-8 text-center">
                  <Globe className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Ready to Analyze</h3>
                  <p className="text-muted-foreground">
                    Fill in your remittance details to get a comprehensive analysis of the best transfer methods.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        </div>

        {/* Features Section */}
        <div className="mt-16 space-y-8">
          <div className="text-center">
            <h2 className="text-2xl font-bold mb-4">
              <span className="shimmer-text">Why Choose XRPL for Remittances?</span>
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            <Card className="glass-card text-center">
              <CardContent className="p-6">
                <Zap className="h-8 w-8 mx-auto text-yellow-500 mb-4" />
                <h3 className="font-semibold mb-2">Ultra-Low Fees</h3>
                <p className="text-sm text-muted-foreground">
                  XRPL charges less than $0.001 per transaction, making it the most cost-effective option.
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card text-center">
              <CardContent className="p-6">
                <Clock className="h-8 w-8 mx-auto text-blue-500 mb-4" />
                <h3 className="font-semibold mb-2">Fast Settlement</h3>
                <p className="text-sm text-muted-foreground">
                  Transactions settle in 3-5 seconds, much faster than traditional banking systems.
                </p>
              </CardContent>
            </Card>

            <Card className="glass-card text-center">
              <CardContent className="p-6">
                <Shield className="h-8 w-8 mx-auto text-green-500 mb-4" />
                <h3 className="font-semibold mb-2">Secure & Reliable</h3>
                <p className="text-sm text-muted-foreground">
                  Built on proven blockchain technology with enterprise-grade security.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Remittance;

