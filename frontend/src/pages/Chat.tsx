import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Header } from "@/components/Header";
import { VoiceCallInterface } from "@/components/VoiceCallInterface";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useState, useEffect, useRef } from "react";
import { Send, Phone, PhoneOff, Loader2, Mic, Volume2, Globe, TrendingUp, PiggyBank, CreditCard, Calculator, FileText, Sparkles, MessageSquare } from "lucide-react";
import { useLocation } from "react-router-dom";
import { useToast } from "@/hooks/use-toast";
import { apiClient, ChatMessage } from "@/lib/api";
const Chat = () => {
  const location = useLocation();
  const {
    toast
  } = useToast();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [inputCount, setInputCount] = useState(0);
  const [isInCall, setIsInCall] = useState(false);
  const [placeholderIndex, setPlaceholderIndex] = useState(0);
  const placeholders = ["Ask about your credit score…", "Type your question in any language…", "Need help with taxes?"];
  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(authStatus);

    // Rotate placeholders every 3 seconds
    const interval = setInterval(() => {
      setPlaceholderIndex(prev => (prev + 1) % placeholders.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);
  const [message, setMessage] = useState("");
  const [language, setLanguage] = useState("en");
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState("chat");
  const [messages, setMessages] = useState<ChatMessage[]>([{
    id: "1",
    sender: "ai",
    text: "Hello! I'm MoneyLingo, your AI financial assistant. I can help you with budgeting, investing, credit, taxes, and more in your preferred language. What would you like to know?",
    time: "10:30 AM"
  }]);

  // Financial quick actions
  const financialTopics = [
    { icon: PiggyBank, label: "Budgeting", prompt: "Help me create a budget" },
    { icon: TrendingUp, label: "Investing", prompt: "Explain investment basics" },
    { icon: CreditCard, label: "Credit Score", prompt: "How do I improve my credit score?" },
    { icon: Calculator, label: "Taxes", prompt: "Help me understand tax deductions" },
    { icon: FileText, label: "Loans", prompt: "Compare loan options" },
    { icon: Globe, label: "Remittances", prompt: "Best way to send money internationally" }
  ];

  // Language options with better support
  const languageOptions = [
    { code: "en", name: "English", flag: "🇺🇸" },
    { code: "es", name: "Español", flag: "🇪🇸" },
    { code: "fr", name: "Français", flag: "🇫🇷" },
    { code: "de", name: "Deutsch", flag: "🇩🇪" },
    { code: "it", name: "Italiano", flag: "🇮🇹" },
    { code: "pt", name: "Português", flag: "🇵🇹" },
    { code: "zh", name: "中文", flag: "🇨🇳" },
    { code: "ja", name: "日本語", flag: "🇯🇵" },
    { code: "ko", name: "한국어", flag: "🇰🇷" },
    { code: "ar", name: "العربية", flag: "🇸🇦" },
    { code: "hi", name: "हिन्दी", flag: "🇮🇳" },
    { code: "ru", name: "Русский", flag: "🇷🇺" }
  ];
  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    setIsLoading(true);

    // Increment input count
    const newCount = inputCount + 1;
    setInputCount(newCount);

    // Show reminder on second input if not authenticated
    if (newCount === 2 && !isAuthenticated) {
      toast({
        title: "💡 Sign in to save your conversations",
        description: "Your chat history will be saved and accessible across devices when you create an account.",
        duration: 6000
      });
    }

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      sender: "user",
      text: messageText,
      time: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit"
      })
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      // Call backend API
      const response = await apiClient.sendChatMessage(messageText, language);
      
      if (response.success && response.data) {
        const aiMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "ai",
          text: response.data.response || "I understand your question. Let me help you with that...",
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
          }),
          audioUrl: response.data.audioUrl
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        // Fallback response if API fails
        const aiMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          sender: "ai",
          text: "I understand your question. Let me explain that in simple terms...",
          time: new Date().toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit"
          })
        };
        setMessages(prev => [...prev, aiMessage]);
        
        toast({
          title: "⚠️ Using offline mode",
          description: "Backend connection failed. Showing sample response.",
          duration: 3000
        });
      }
    } catch (error) {
      console.error('Chat API error:', error);
      toast({
        title: "❌ Connection error",
        description: "Unable to connect to the AI assistant. Please try again.",
        duration: 3000
      });
    } finally {
      setIsLoading(false);
      setMessage("");
    }
  };

  const handleQuickTopic = (prompt: string) => {
    setMessage(prompt);
    handleSendMessage(prompt);
  };

  const handleVoiceSynthesis = async (text: string) => {
    if (!text.trim()) return;
    
    try {
      if ('speechSynthesis' in window) {
        // Stop any current speech
        speechSynthesis.cancel();
        
        // Create speech utterance
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.8;
        utterance.pitch = 1;
        utterance.volume = 1;
        utterance.lang = language === 'en' ? 'en-US' : language;
        
        // Set up event listeners
        utterance.onstart = () => {
          toast({
            title: "🎤 AI Speaking",
            description: "MoneyLingo is responding with voice",
            duration: 2000
          });
        };
        
        utterance.onerror = (e) => {
          console.error('Speech synthesis error:', e);
          toast({
            title: "❌ Speech Error",
            description: "Failed to speak text",
            variant: "destructive"
          });
        };
        
        // Start speaking
        speechSynthesis.speak(utterance);
      } else {
        toast({
          title: "❌ Speech Not Supported",
          description: "Your browser doesn't support speech synthesis",
          variant: "destructive"
        });
      }
    } catch (error) {
      console.error('Voice synthesis error:', error);
      toast({
        title: "❌ Speech Error",
        description: "Failed to start speech synthesis",
        variant: "destructive"
      });
    }
  };

  // Handle initial message from homepage
  useEffect(() => {
    const initialMessage = location.state?.initialMessage;
    if (initialMessage) {
      setMessage(initialMessage);
      // Auto-send the message
      setTimeout(() => {
        handleSendMessage(initialMessage);
      }, 100);
    }
  }, [location.state]);
  const handleSend = () => {
    if (!message.trim()) return;
    handleSendMessage(message);
  };
  const toggleCall = () => {
    setIsInCall(!isInCall);
  };
  const endCall = () => {
    setIsInCall(false);
  };
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth"
    });
  };
  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  return <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background Gradients - Same as homepage */}
      <div className="absolute inset-0 bg-gradient-main pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-clouds pointer-events-none" />
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-background/5 to-background/20 pointer-events-none" />
      
      {/* Floating decorative elements */}
      <div className="absolute top-20 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <Header />

      {/* Main Content Area */}
      <main className="flex-1 relative z-10 container mx-auto max-w-6xl px-4 py-6">
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-6">
            <TabsTrigger value="chat" className="flex items-center gap-2">
              <MessageSquare className="h-4 w-4" />
              Chat
            </TabsTrigger>
            <TabsTrigger value="voice" className="flex items-center gap-2">
              <Mic className="h-4 w-4" />
              Voice
            </TabsTrigger>
            <TabsTrigger value="topics" className="flex items-center gap-2">
              <Sparkles className="h-4 w-4" />
              Quick Topics
            </TabsTrigger>
          </TabsList>

          <TabsContent value="chat" className="space-y-6">
            {/* Chat Messages */}
            <Card className="h-96 overflow-y-auto">
              <CardContent className="p-4 space-y-4">
                {messages.map((msg) => (
                  <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[80%] rounded-2xl p-4 ${
                      msg.sender === 'user' 
                        ? 'bg-primary text-primary-foreground' 
                        : 'bg-muted'
                    }`}>
                      <p className="text-sm">{msg.text}</p>
                      <div className="flex items-center justify-between mt-2">
                        <span className="text-xs opacity-70">{msg.time}</span>
                        {msg.sender === 'ai' && (
                          <Button
                            size="sm"
                            variant="ghost"
                            onClick={() => handleVoiceSynthesis(msg.text)}
                            className="h-6 w-6 p-0"
                          >
                            <Volume2 className="h-3 w-3" />
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="voice" className="space-y-6">
            {/* Voice Call Interface */}
            <div className="text-center space-y-6 animate-fade-in-up max-w-3xl mx-auto px-4">
              <div>
                <h2 className="text-2xl sm:text-3xl font-bold leading-tight">
                  <span className="block shimmer-text pb-2">Voice Conversation</span>
                </h2>
                <p className="text-sm sm:text-base text-muted-foreground mt-2">
                  Speak naturally about any financial topic in your language
                </p>
              </div>

              {/* Large Voice Call Button */}
              <div className="flex flex-col items-center gap-6">
                <Button 
                  size="icon" 
                  onClick={toggleCall} 
                  className="rounded-full transition-all hover:scale-105 shadow-2xl border-0"
                  style={{
                    width: '220px',
                    height: '220px',
                    background: isInCall 
                      ? 'hsl(var(--destructive))' 
                      : 'linear-gradient(135deg, hsl(180, 62%, 35%), hsl(192, 81%, 50%), hsl(25, 95%, 63%))',
                    backgroundSize: '200% 200%',
                    animation: isInCall ? 'none' : 'gradient-wave-animation 8s ease infinite'
                  }}
                  aria-label={isInCall ? "End call" : "Start voice call"}
                >
                  {isInCall ? <PhoneOff className="h-20 w-20" /> : <Phone className="h-20 w-20 text-white" />}
                </Button>
                
                <div className="text-center">
                  <p className="text-lg sm:text-xl font-semibold mb-1">
                    {isInCall ? "Talking to MoneyLingo..." : "Tap to start talking"}
                  </p>
                  <p className="text-xs sm:text-sm text-muted-foreground">
                    {isInCall ? "We're listening and ready to help" : "Natural conversation in your language"}
                  </p>
                </div>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="topics" className="space-y-6">
            {/* Financial Quick Topics */}
            <div className="text-center space-y-4 mb-6">
              <h2 className="text-2xl font-bold">
                <span className="shimmer-text">Quick Financial Topics</span>
              </h2>
              <p className="text-muted-foreground">
                Click any topic to start a conversation
              </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              {financialTopics.map((topic, index) => {
                const IconComponent = topic.icon;
                return (
                  <Card 
                    key={index}
                    className="cursor-pointer hover:shadow-lg transition-all duration-300 hover:scale-105"
                    onClick={() => handleQuickTopic(topic.prompt)}
                  >
                    <CardContent className="p-6 text-center space-y-3">
                      <IconComponent className="h-8 w-8 mx-auto text-primary" />
                      <h3 className="font-semibold">{topic.label}</h3>
                      <p className="text-sm text-muted-foreground">{topic.prompt}</p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </TabsContent>
        </Tabs>
      </main>

      {/* Fixed Chat Bar at Bottom */}
      <div className="relative z-20">
        <div className="px-4 py-4 container mx-auto max-w-4xl">
          <div className="glass-card p-4 rounded-3xl shadow-xl space-y-4">
            {/* Language Selection */}
            <div className="flex items-center gap-2">
              <Globe className="h-4 w-4 text-muted-foreground" />
              <Select value={language} onValueChange={setLanguage}>
                <SelectTrigger className="w-48">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {languageOptions.map((lang) => (
                    <SelectItem key={lang.code} value={lang.code}>
                      <span className="flex items-center gap-2">
                        <span>{lang.flag}</span>
                        <span>{lang.name}</span>
                      </span>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Badge variant="secondary" className="ml-auto">
                {languageOptions.find(l => l.code === language)?.name}
              </Badge>
            </div>

            {/* Message Input */}
            <div className="flex items-center gap-2">
              <Input 
                placeholder={placeholders[placeholderIndex]} 
                value={message} 
                onChange={e => setMessage(e.target.value)} 
                onKeyPress={handleKeyPress} 
                className="h-12 text-base rounded-3xl bg-transparent border-0 focus-visible:ring-0 focus-visible:ring-offset-0 pr-12" 
                aria-label="Message input" 
              />
              <Button 
                size="icon" 
                onClick={handleSend} 
                disabled={!message.trim() || isLoading} 
                className="h-10 w-10 rounded-full bg-gradient-primary hover:scale-110 transition-all shadow-lg disabled:opacity-50 flex-shrink-0" 
                aria-label="Send message"
              >
                {isLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              </Button>
            </div>

            <p className="text-xs text-muted-foreground text-center">
              💡 Ask about budgeting, investing, credit, taxes, or any financial topic • MoneyLingo can make mistakes
            </p>
          </div>
        </div>
      </div>

      {/* Voice Call Interface */}
      <VoiceCallInterface isActive={isInCall} onEnd={endCall} />
    </div>;
};
export default Chat;