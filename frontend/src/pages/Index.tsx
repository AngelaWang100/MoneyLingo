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
import { MessageSquare, FileText, Shield, Globe, TrendingUp, Headphones, Heart, Users, Target, Send, Mic, PiggyBank, CheckCircle2, CreditCard, Wallet, TrendingDown, Phone, Sparkles } from "lucide-react";
import { VoiceCallInterface } from "@/components/VoiceCallInterface";
import { useToast } from "@/hooks/use-toast";
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
  const placeholders = ["Ask about your credit score…", "Type your question in any language…", "Need help with taxes?", "How do I build credit?", "What's a good interest rate?"];
  const languages = [{
    code: "en",
    name: "English",
    flag: "🇺🇸",
    greeting: "How can I help you today?"
  }, {
    code: "es",
    name: "Español",
    flag: "🇪🇸",
    greeting: "¿Cómo puedo ayudarte hoy?"
  }, {
    code: "zh",
    name: "中文",
    flag: "🇨🇳",
    greeting: "今天我能帮你什么？"
  }, {
    code: "ar",
    name: "العربية",
    flag: "🇸🇦",
    greeting: "كيف يمكنني مساعدتك اليوم؟"
  }, {
    code: "hi",
    name: "हिन्दी",
    flag: "🇮🇳",
    greeting: "आज मैं आपकी कैसे मदद कर सकता हूं?"
  }, {
    code: "fr",
    name: "Français",
    flag: "🇫🇷",
    greeting: "Comment puis-je vous aider aujourd'hui?"
  }];
  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(authStatus);

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
  }, []);
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
    title: "Welcome to MoneyLingo",
    description: "Your AI-powered financial literacy assistant in your native language.",
    icon: PiggyBank
  }, {
    title: "Upload & Analyze",
    description: "Upload your credit statements, tax forms, or any financial document for instant analysis.",
    icon: FileText
  }, {
    title: "Get Personalized Plans",
    description: "Receive customized financial strategies tailored to your goals and situation.",
    icon: Target
  }];
  const features = [{
    icon: MessageSquare,
    title: "AI Financial Assistant",
    description: "Get instant answers to your financial questions in your native language. Our AI breaks down complex concepts into simple, culturally-aware guidance through natural conversation.",
    link: "/chat"
  }, {
    icon: FileText,
    title: "Document Analysis",
    description: "Upload tax forms, credit statements, bank documents, or any financial paperwork for instant analysis. Receive clear explanations and actionable insights in seconds.",
    link: "/documents"
  }, {
    icon: Target,
    title: "Personalized Financial Plans",
    description: "Create customized financial strategies tailored to your goals and situation. Track your progress, build credit, manage debt, and achieve financial confidence.",
    link: "/dashboard"
  }];
  const values = [{
    icon: Heart,
    title: "Empathy First",
    description: "We understand the challenges immigrants and ESL speakers face in navigating complex financial systems."
  }, {
    icon: Users,
    title: "Cultural Inclusivity",
    description: "Financial advice that respects and incorporates diverse cultural perspectives and experiences."
  }, {
    icon: Target,
    title: "Clear Communication",
    description: "Breaking down complex financial jargon into simple, accessible language everyone can understand."
  }, {
    icon: Shield,
    title: "Trust & Security",
    description: "Your financial information is protected with the highest security standards in the industry."
  }];
  const faqs = [{
    question: "How does the AI understand my native language?",
    answer: "Our AI is trained on multiple languages and financial terminology across cultures. It can understand and respond accurately in over 25 languages, ensuring you get precise financial guidance in the language you're most comfortable with."
  }, {
    question: "Is my financial data secure?",
    answer: "Yes! We use bank-level encryption (256-bit SSL) to protect all your documents and data. Your information is encrypted both in transit and at rest, and we never share your data with third parties. All staff undergo background checks and security training."
  }, {
    question: "What types of documents can I upload?",
    answer: "You can upload tax forms (W-2, 1040, etc.), credit card statements, bank statements, loan documents, and more. We support PDF, JPG, and PNG formats up to 10MB per file."
  }, {
    question: "How accurate is the AI's financial advice?",
    answer: "Our AI is trained on official financial regulations and best practices, but it's important to note that it provides educational guidance, not personalized financial advice. For specific financial decisions, we recommend consulting with a licensed financial advisor."
  }, {
    question: "Can I use voice input if I'm not comfortable typing?",
    answer: "Absolutely! Our platform supports voice input in multiple languages. Simply click the phone icon to start a voice call with our AI assistant. The AI will understand and respond to your questions naturally."
  }, {
    question: "How much does MoneyLingo cost?",
    answer: "We offer a free tier with basic features including AI chat and document uploads. Premium plans start at $9.99/month and include unlimited AI sessions, priority support, and advanced analytics features."
  }, {
    question: "What languages are currently supported?",
    answer: "We currently support English, Spanish, Mandarin Chinese, Arabic, Hindi, French, Portuguese, Russian, Korean, Japanese, Vietnamese, Tagalog, and many more. We're constantly adding new languages based on user demand."
  }, {
    question: "Can the AI help me build my credit score?",
    answer: "Yes! The AI can provide personalized credit-building strategies, explain how credit scores work, help you understand your credit report, and suggest specific actions to improve your score based on your situation."
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
              <span className="block shimmer-text pb-2">Talk to Your Financial AI</span>
            </h1>
            <p className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto px-4 sm:px-6">
              Get instant answers to your financial questions in your native language. Our AI assistant breaks down complex concepts into simple, culturally-aware guidance.
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
              <p className="text-xs sm:text-sm text-muted-foreground mt-4 text-center animate-fade-in">Available 24/7 in 20+ languages</p>
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
                Everything You Need to Succeed
              </h2>
              <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                Comprehensive tools to build your financial confidence and achieve your goals.
              </p>
            </div>

            <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {features.map((feature, index) => {
              const Icon = feature.icon;
              const FeatureCard = feature.link ? Link : 'div';
              return <FeatureCard key={feature.title} to={feature.link} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md p-8 rounded-2xl hover:shadow-xl hover:-translate-y-2 transition-all duration-300 group animate-fade-in-up cursor-pointer" style={{
                animationDelay: `${index * 0.1}s`
              }}>
                    <div className="h-14 w-14 rounded-xl bg-gradient-primary flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300 shadow-lg">
                      <Icon className="h-7 w-7 text-primary-foreground" />
                    </div>
                    <h3 className="text-xl font-semibold mb-3">{feature.title}</h3>
                    <p className="text-base text-muted-foreground leading-relaxed">{feature.description}</p>
                  </FeatureCard>;
            })}
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
                  Frequently Asked Questions
                </h2>
                <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
                  Find answers to common questions about MoneyLingo
                </p>
              </div>

              <Accordion type="single" collapsible className="space-y-4">
                {faqs.map((faq, index) => <AccordionItem key={index} value={`item-${index}`} className="bg-background/80 backdrop-blur-sm border border-border/40 shadow-md rounded-lg px-6 hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 animate-fade-in-up" style={{
                animationDelay: `${index * 0.05}s`
              }}>
                    <AccordionTrigger className="text-left hover:no-underline">
                      <span className="font-semibold">{faq.question}</span>
                    </AccordionTrigger>
                    <AccordionContent className="text-muted-foreground">
                      {faq.answer}
                    </AccordionContent>
                  </AccordionItem>)}
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
                Join thousands of users who are building financial confidence in their native language.
              </p>
              <Button size="lg" onClick={handleGetStarted} className="bg-gradient-glow text-white px-12 py-7 text-xl rounded-full hover:scale-105 hover:shadow-2xl transition-all duration-300 shadow-xl glow-pulse">
                Get Started Free
              </Button>
              <p className="text-sm text-muted-foreground mt-4">
                No credit card required • Available in 20+ languages
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
              Sign in required
            </AlertDialogTitle>
            <AlertDialogDescription className="text-base">
              You need to sign in to chat with our AI assistant and get personalized financial guidance in your language.
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