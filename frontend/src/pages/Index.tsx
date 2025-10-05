import React, { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { AlertDialog, AlertDialogAction, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle } from "@/components/ui/alert-dialog";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Link, useNavigate } from "react-router-dom";
import { MessageSquare, FileText, Shield, Globe, TrendingUp, Headphones, Heart, Users, Target, Send, Mic, PiggyBank, CheckCircle2, CreditCard, Wallet, TrendingDown, Phone, Sparkles, Loader2 } from "lucide-react";
import { VoiceCallInterface } from "@/components/VoiceCallInterface";
import { useToast } from "@/hooks/use-toast";
import { apiClient } from "@/lib/api";
const Index = () => {
  const navigate = useNavigate();
  const {
    toast
  } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [showAuthDialog, setShowAuthDialog] = useState(false);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [onboardingStep, setOnboardingStep] = useState(0);
  const [selectedLanguage, setSelectedLanguage] = useState("English");
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const [isCallActive, setIsCallActive] = useState(false);
  const [scrollProgress, setScrollProgress] = useState(0);
  
  // AI-powered dynamic content
  const [aiContent, setAiContent] = useState({
    heroTitle: "Talk to Your Financial AI",
    heroDescription: "AI-powered financial guidance in your language.",
    features: [],
    faqs: [],
    isLoading: true
  });
  const placeholders = ["Ask about your credit score…", "Type your question in any language…", "Need help with taxes?", "How do I build credit?", "What's a good interest rate?"];
  const languages = [{
    code: "en",
    name: "English",
    flag: "🇺🇸"
  }, {
    code: "es",
    name: "Español",
    flag: "🇪🇸"
  }, {
    code: "zh",
    name: "中文",
    flag: "🇨🇳"
  }, {
    code: "ar",
    name: "العربية",
    flag: "🇸🇦"
  }, {
    code: "hi",
    name: "हिन्दी",
    flag: "🇮🇳"
  }, {
    code: "fr",
    name: "Français",
    flag: "🇫🇷"
  }];
  // Load AI-generated content
  const loadAIContent = async () => {
    try {
      setAiContent(prev => ({ ...prev, isLoading: true }));
      
      // Get AI-generated features
      const featuresResponse = await apiClient.sendChatMessage(
        "Generate 3 key features for a financial AI assistant website. Return as JSON array with title, description, and icon fields.",
        selectedLanguage
      );
      
      // Get AI-generated FAQs
      const faqResponse = await apiClient.sendChatMessage(
        "Generate 5 common FAQ questions and answers for a financial AI assistant. Return as JSON array with question and answer fields.",
        selectedLanguage
      );
      
      if (featuresResponse.success && faqResponse.success) {
        setAiContent(prev => ({
          ...prev,
          features: featuresResponse.data?.response ? JSON.parse(featuresResponse.data.response) : [],
          faqs: faqResponse.data?.response ? JSON.parse(faqResponse.data.response) : [],
          isLoading: false
        }));
      }
    } catch (error) {
      console.error('Failed to load AI content:', error);
      setAiContent(prev => ({ ...prev, isLoading: false }));
    }
  };

  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(authStatus);

    // Load AI content
    loadAIContent();

    // Rotate placeholders every 3 seconds
    const interval = setInterval(() => {
      setPlaceholderIndex(prev => (prev + 1) % placeholders.length);
    }, 3000);

    // Scroll progress tracking
    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const progress = window.scrollY / totalHeight * 100;
      setScrollProgress(progress);
    };
    window.addEventListener('scroll', handleScroll);
    return () => {
      clearInterval(interval);
      window.removeEventListener('scroll', handleScroll);
    };
  }, [selectedLanguage]);
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    if (isAuthenticated) {
      navigate('/chat', {
        state: {
          initialMessage: searchQuery
        }
      });
    } else {
      setShowAuthDialog(true);
    }
  };
  const handleVoiceInput = () => {
    toast({
      title: "Voice input",
      description: "Voice recognition feature coming soon!"
    });
  };
  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/dashboard');
    } else {
      setShowOnboarding(true);
    }
  };
  const onboardingSteps = [{
    title: "AI Financial Assistant",
    description: "Connect with our AI for personalized financial guidance.",
    icon: PiggyBank
  }, {
    title: "Document Analysis",
    description: "Upload financial documents for AI-powered analysis.",
    icon: FileText
  }, {
    title: "Personalized Plans",
    description: "Get customized financial strategies from our AI.",
    icon: Target
  }];
  const features = [{
    icon: MessageSquare,
    title: "AI Financial Assistant",
    description: "AI-powered financial assistance with real-time responses.",
    link: "/chat"
  }, {
    icon: FileText,
    title: "Document Analysis",
    description: "AI-powered document analysis with instant insights.",
    link: "/documents"
  }, {
    icon: Target,
    title: "Personalized Financial Plans",
    description: "AI-generated personalized financial strategies and tracking.",
    link: "/dashboard"
  }];
  const values = [{
    icon: Heart,
    title: "AI-Powered Empathy",
    description: "AI-driven understanding of financial challenges."
  }, {
    icon: Users,
    title: "AI Cultural Intelligence",
    description: "AI-powered cultural awareness in financial guidance."
  }, {
    icon: Target,
    title: "AI Communication",
    description: "AI-generated clear and accessible financial language."
  }, {
    icon: Shield,
    title: "AI Security",
    description: "AI-powered financial data protection."
  }];
  const faqs = [{
    question: "How does the AI understand my native language?",
    answer: "AI-powered multilingual support with real-time language processing."
  }, {
    question: "Is my financial data secure?",
    answer: "Advanced security with AI-powered data protection."
  }, {
    question: "What types of documents can I upload?",
    answer: "AI-powered document analysis for various financial formats."
  }, {
    question: "How accurate is the AI's financial advice?",
    answer: "AI-generated guidance based on real-time financial data analysis."
  }, {
    question: "Can I use voice input if I'm not comfortable typing?",
    answer: "AI-powered voice recognition and response in multiple languages."
  }, {
    question: "How much does MoneyLingo cost?",
    answer: "AI-powered financial assistance with flexible pricing."
  }, {
    question: "What languages are currently supported?",
    answer: "AI supports multiple languages with real-time translation."
  }, {
    question: "Can the AI help me build my credit score?",
    answer: "AI-powered credit analysis and personalized recommendations."
  }];
  const currentLanguage = languages.find(l => l.name === selectedLanguage) || languages[0];
  return <div className="min-h-screen flex flex-col bg-background relative">
      {/* Scroll Progress Bar */}
      <div className="fixed top-0 left-0 right-0 h-1 bg-border/20 z-50">
        <div className="h-full bg-gradient-primary transition-all duration-150 ease-out" style={{
        width: `${scrollProgress}%`
      }} />
      </div>
      
      <Header />

      <main className="flex-1 relative overflow-hidden">
        {/* Floating mascot */}
        <TooltipProvider>
          <div className="fixed bottom-8 right-8 z-50">
            <Tooltip>
              <TooltipTrigger asChild>
                <button className="relative group cursor-pointer bounce-gentle focus:outline-none" onClick={() => navigate('/chat')} aria-label="Chat with AI">
                  <div className="relative">
                    <PiggyBank className="h-16 w-16 text-primary drop-shadow-lg transition-all duration-300 group-hover:scale-110 group-hover:drop-shadow-2xl" />
                    {/* Glow effect on hover */}
                    <div className="absolute inset-0 rounded-full bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  </div>
                </button>
              </TooltipTrigger>
              <TooltipContent side="left">
                <p className="font-medium">Need help? Click me! 👋</p>
              </TooltipContent>
            </Tooltip>
          </div>
        </TooltipProvider>
        
        {/* Hero Section with radial gradient background */}
        <section className="relative px-6 pt-24 pb-32 z-10" style={{
        background: 'radial-gradient(ellipse 100% 60% at 50% 0%, hsl(192, 100%, 97%), hsl(0, 0%, 100%) 70%)'
      }}>
          <div className="container mx-auto max-w-6xl text-center space-y-8 animate-fade-in-up">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-tight px-4">
              <span className="block shimmer-text pb-2">
                {aiContent.isLoading ? (
                  <div className="flex items-center gap-2">
                    <Loader2 className="h-8 w-8 animate-spin" />
                    <span>Loading AI Content...</span>
                  </div>
                ) : (
                  aiContent.heroTitle
                )}
              </span>
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto px-4 sm:px-6">
              {aiContent.isLoading ? "Generating AI content..." : aiContent.heroDescription}
            </p>
            
            {/* Prominent Call Button */}
            <div className="pt-6 sm:pt-8 px-4">
              <div className="flex flex-col items-center gap-3 animate-fade-in-up">
                <Button onClick={() => setIsCallActive(true)} size="lg" className="h-16 px-10 bg-gradient-glow text-white rounded-full hover:scale-105 transition-all duration-300 shadow-2xl glow-pulse text-lg font-semibold">
                  <Phone className="h-6 w-6 mr-3 animate-pulse" />
                  Talk to AI Assistant Now
                </Button>
                <p className="text-xs text-muted-foreground flex items-center gap-1.5">
                  <Headphones className="h-3.5 w-3.5" />
                  Instant voice guidance in your language
                </p>
              </div>
              
              {/* Language Selector - Moved Below Call Button */}
              <div className="flex justify-center gap-2 flex-wrap mt-8">
                {languages.slice(0, 6).map(lang => <button key={lang.code} onClick={() => setSelectedLanguage(lang.name)} className={`px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-300 ${selectedLanguage === lang.name ? 'bg-primary text-primary-foreground shadow-md scale-105' : 'bg-background/60 backdrop-blur-sm border border-border/40 hover:border-primary/40 hover:scale-105'}`}>
                    <span className="mr-1.5">{lang.flag}</span>
                    {lang.name}
                  </button>)}
              </div>
              <p className="text-xs sm:text-sm text-muted-foreground mt-4 text-center animate-fade-in">AI-powered multilingual support</p>
            </div>
          </div>
        </section>

        {/* Smooth gradient transition to features */}
        <div className="relative h-20 -mt-16" style={{
        background: 'linear-gradient(to bottom, hsl(0, 0%, 100%), hsl(192, 100%, 98%))'
      }} />

        {/* Features Section with soft background and overlapping top */}
        <section className="relative px-6 py-24 -mt-24 z-20" style={{
        backgroundColor: 'hsl(192, 100%, 98%)'
      }}>
          <div className="container mx-auto max-w-6xl relative">
            {/* Overlapping decorative element */}
            <div className="absolute -top-16 left-1/2 -translate-x-1/2 w-24 h-24 bg-gradient-primary rounded-full blur-3xl opacity-20" />
            
            <div className="text-center mb-16 animate-fade-in-up">
              <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 shimmer-text">
                AI-Powered Financial Tools
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                AI-driven financial assistance and guidance.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {aiContent.isLoading ? (
                // Loading state
                Array.from({ length: 3 }).map((_, index) => (
                  <div key={index} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md p-8 rounded-2xl animate-pulse">
                    <div className="h-14 w-14 rounded-xl bg-muted mb-6"></div>
                    <div className="h-6 bg-muted rounded mb-3"></div>
                    <div className="h-4 bg-muted rounded mb-2"></div>
                    <div className="h-4 bg-muted rounded w-3/4"></div>
                  </div>
                ))
              ) : (
                // AI-generated features
                aiContent.features.map((feature: any, index: number) => (
                  <div key={index} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md p-8 rounded-2xl hover:shadow-xl hover:-translate-y-2 transition-all duration-300 group animate-fade-in-up" style={{
                    animationDelay: `${index * 0.1}s`
                  }}>
                    <div className="h-14 w-14 rounded-xl bg-gradient-primary flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                      <MessageSquare className="h-7 w-7 text-primary-foreground" />
                    </div>
                    <h3 className="text-xl font-semibold mb-3">{feature.title || 'AI Feature'}</h3>
                    <p className="text-base text-muted-foreground leading-relaxed">{feature.description || 'AI-powered financial assistance'}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </section>
        
        {/* Smooth gradient transition to FAQ */}
        <div className="relative h-24" style={{
        background: 'linear-gradient(to bottom, hsl(192, 100%, 98%), hsl(210, 60%, 98%))'
      }}>
          <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-primary/10 rounded-full blur-3xl" />
        </div>
        
        {/* FAQ Section with subtle tint and overlapping top */}
        <section id="faq" className="relative px-6 py-24 -mt-12 z-20" style={{
        backgroundColor: 'hsl(210, 60%, 98%)'
      }}>
          <div className="container mx-auto max-w-6xl relative">
            <div className="max-w-4xl mx-auto">
              <div className="text-center mb-16 animate-fade-in-up">
                <h2 className="text-3xl sm:text-4xl md:text-5xl font-bold mb-6 shimmer-text">
                  AI-Powered FAQ
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  AI-generated answers to your questions
                </p>
              </div>

              <Accordion type="single" collapsible className="space-y-4">
                {aiContent.isLoading ? (
                  // Loading state
                  Array.from({ length: 5 }).map((_, index) => (
                    <div key={index} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md rounded-lg px-6 py-4 animate-pulse">
                      <div className="h-6 bg-muted rounded mb-2"></div>
                      <div className="h-4 bg-muted rounded w-3/4"></div>
                    </div>
                  ))
                ) : (
                  // AI-generated FAQs
                  aiContent.faqs.map((faq: any, index: number) => (
                    <AccordionItem key={index} value={`item-${index}`} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md rounded-lg px-6 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 animate-fade-in-up" style={{
                      animationDelay: `${index * 0.05}s`
                    }}>
                      <AccordionTrigger className="text-left hover:no-underline">
                        <span className="font-semibold">{faq.question || 'AI-Generated Question'}</span>
                      </AccordionTrigger>
                      <AccordionContent className="text-muted-foreground">
                        {faq.answer || 'AI-generated answer'}
                      </AccordionContent>
                    </AccordionItem>
                  ))
                )}
              </Accordion>
            </div>
          </div>
        </section>
        
        {/* Smooth gradient transition to CTA */}
        <div className="relative h-24" style={{
        background: 'linear-gradient(to bottom, hsl(210, 60%, 98%), hsl(0, 0%, 100%))'
      }}>
          <div className="absolute top-1/2 left-1/4 w-40 h-40 bg-accent/10 rounded-full blur-3xl" />
          <div className="absolute top-1/2 right-1/4 w-40 h-40 bg-primary/10 rounded-full blur-3xl" />
        </div>
        
        {/* CTA Section with radial gradient background and overlapping */}
        <section className="relative px-6 py-28 -mt-12 z-20" style={{
        background: 'radial-gradient(ellipse 100% 80% at 50% 50%, hsl(192, 100%, 97%), hsl(210, 60%, 96%))'
      }}>
          <div className="container mx-auto max-w-6xl relative">
            {/* Decorative elements */}
            <div className="absolute -top-20 left-10 w-32 h-32 bg-primary/10 rounded-full blur-3xl animate-pulse-slow" />
            <div className="absolute -bottom-10 right-10 w-40 h-40 bg-accent/10 rounded-full blur-3xl animate-float" />
            
            <div className="max-w-4xl mx-auto text-center bg-background/90 backdrop-blur-sm border border-border/40 shadow-2xl p-12 sm:p-16 rounded-3xl relative z-10 animate-fade-in-up">
              <h2 className="text-4xl md:text-5xl font-bold mb-6 shimmer-text">
                Ready to Take Control of Your Finances?
              </h2>
              <p className="text-xl text-muted-foreground mb-10 max-w-2xl mx-auto leading-relaxed">
                Start your AI-powered financial journey today.
              </p>
              <Button size="lg" onClick={handleGetStarted} className="bg-gradient-glow text-white px-12 py-7 text-xl rounded-full hover:scale-105 hover:shadow-2xl transition-all duration-300 shadow-xl glow-pulse">
                Get Started Free
              </Button>
              <p className="text-sm text-muted-foreground mt-4">
                AI-powered financial assistance
              </p>
            </div>
          </div>
        </section>
      </main>

      <Footer />
      
      {/* Voice Call Interface */}
      <VoiceCallInterface isActive={isCallActive} onEnd={() => setIsCallActive(false)} />

      {/* Auth Required Dialog */}
      <AlertDialog open={showAuthDialog} onOpenChange={setShowAuthDialog}>
        <AlertDialogContent className="glass-card border-2 border-primary/20">
          <AlertDialogHeader>
            <AlertDialogTitle className="text-2xl shimmer-text pb-1">
              AI Access Required
            </AlertDialogTitle>
            <AlertDialogDescription className="text-base">
              Sign in to access AI-powered financial assistance.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter className="flex-col sm:flex-row gap-2">
            <Button variant="outline" onClick={() => setShowAuthDialog(false)} className="hover-lift">
              Cancel
            </Button>
            <Button asChild className="bg-gradient-primary hover-lift shadow-lg">
              <Link to="/signin">Sign In</Link>
            </Button>
            <Button asChild variant="secondary" className="hover-lift">
              <Link to="/signup">Create Account</Link>
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
      
      {/* Onboarding Dialog */}
      <Dialog open={showOnboarding} onOpenChange={setShowOnboarding}>
        <DialogContent className="glass-card max-w-lg">
          <DialogHeader>
            <DialogTitle className="text-2xl shimmer-text text-center mb-4">
              {onboardingSteps[onboardingStep].title}
            </DialogTitle>
            <DialogDescription className="text-center text-base">
              {onboardingSteps[onboardingStep].description}
            </DialogDescription>
          </DialogHeader>
          
          <div className="flex justify-center my-8">
            {(() => {
            const IconComponent = onboardingSteps[onboardingStep].icon;
            return <IconComponent className="h-24 w-24 text-primary animate-float" />;
          })()}
          </div>
          
          <div className="flex justify-center gap-2 mb-6">
            {onboardingSteps.map((_, index) => <div key={index} className={`h-2 w-2 rounded-full transition-all duration-300 ${index === onboardingStep ? 'bg-primary w-8' : 'bg-border'}`} />)}
          </div>
          
          <div className="flex gap-3">
            {onboardingStep > 0 && <Button variant="outline" onClick={() => setOnboardingStep(prev => prev - 1)} className="flex-1">
                Back
              </Button>}
            {onboardingStep < onboardingSteps.length - 1 ? <Button onClick={() => setOnboardingStep(prev => prev + 1)} className="flex-1 bg-gradient-primary">
                Next
              </Button> : <Button asChild className="flex-1 bg-gradient-primary">
                <Link to="/signup">Create Account</Link>
              </Button>}
          </div>
        </DialogContent>
      </Dialog>
    </div>;
};
export default Index;