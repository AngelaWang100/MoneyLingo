import { Button } from "@/components/ui/button";
import { PhoneOff, Mic, MicOff, Volume2, Play, Pause, MessageSquare } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { apiClient } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

// TypeScript declarations for Speech Recognition API
declare global {
  interface Window {
    SpeechRecognition: typeof SpeechRecognition;
    webkitSpeechRecognition: typeof SpeechRecognition;
  }
}

interface SpeechRecognition extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  abort(): void;
  onstart: ((this: SpeechRecognition, ev: Event) => any) | null;
  onresult: ((this: SpeechRecognition, ev: SpeechRecognitionEvent) => any) | null;
  onend: ((this: SpeechRecognition, ev: Event) => any) | null;
  onerror: ((this: SpeechRecognition, ev: SpeechRecognitionErrorEvent) => any) | null;
}

interface SpeechRecognitionEvent extends Event {
  resultIndex: number;
  results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
  length: number;
  item(index: number): SpeechRecognitionResult;
  [index: number]: SpeechRecognitionResult;
}

interface SpeechRecognitionResult {
  length: number;
  item(index: number): SpeechRecognitionAlternative;
  [index: number]: SpeechRecognitionAlternative;
  isFinal: boolean;
}

interface SpeechRecognitionAlternative {
  transcript: string;
  confidence: number;
}

interface SpeechRecognitionErrorEvent extends Event {
  error: string;
  message: string;
}

declare var SpeechRecognition: {
  prototype: SpeechRecognition;
  new(): SpeechRecognition;
};

interface VoiceCallInterfaceProps {
  isActive: boolean;
  onEnd: () => void;
}

export const VoiceCallInterface = ({ isActive, onEnd }: VoiceCallInterfaceProps) => {
  const [isMuted, setIsMuted] = useState(false);
  const [isAISpeaking, setIsAISpeaking] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [synthesisText, setSynthesisText] = useState("");
  const [isListening, setIsListening] = useState(false);
  const [recognizedText, setRecognizedText] = useState("");
  const [conversationHistory, setConversationHistory] = useState<Array<{speaker: 'user' | 'ai', text: string}>>([]);
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const recognitionRef = useRef<SpeechRecognition | null>(null);
  const finalTranscriptRef = useRef<string>("");
  const { toast } = useToast();

  // Handle voice synthesis using Web Speech API
  const handleVoiceSynthesis = async (text: string) => {
    if (!text.trim()) {
      console.log('❌ Empty text for synthesis');
      return;
    }
    
    console.log('🔊 Starting voice synthesis:', text);
    setIsProcessing(true);
    setSynthesisText(text);
    
    try {
      if ('speechSynthesis' in window) {
        // Stop any current speech
        speechSynthesis.cancel();
        
        // Create speech utterance
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.8;
        utterance.pitch = 1;
        utterance.volume = 1;
        utterance.lang = 'en-US';
        
        // Set up event listeners
        utterance.onstart = () => {
          console.log('🎤 Speech started');
          setIsAISpeaking(true);
          setIsPlaying(true);
          setIsProcessing(false);
          toast({
            title: "🎤 AI Speaking",
            description: "MoneyLingo is responding with voice",
            duration: 2000
          });
        };
        
        utterance.onend = () => {
          console.log('🔇 Speech ended');
          setIsAISpeaking(false);
          setIsPlaying(false);
        };
        
        utterance.onerror = (e) => {
          console.error('Speech synthesis error:', e);
          setIsAISpeaking(false);
          setIsPlaying(false);
          setIsProcessing(false);
          toast({
            title: "❌ Speech Error",
            description: "Failed to speak text",
            variant: "destructive"
          });
        };
        
        // Start speaking
        console.log('🚀 Starting speech synthesis...');
        speechSynthesis.speak(utterance);
        
        // Store utterance reference for controls (SpeechSynthesisUtterance doesn't have pause/play methods)
        setCurrentAudio(null);
        
      } else {
        toast({
          title: "❌ Speech Not Supported",
          description: "Your browser doesn't support speech synthesis",
          variant: "destructive"
        });
        setIsProcessing(false);
      }
    } catch (error) {
      console.error('Voice synthesis error:', error);
      toast({
        title: "❌ Speech Error",
        description: "Failed to start speech synthesis",
        variant: "destructive"
      });
      setIsProcessing(false);
    }
  };

  // Toggle audio playback
  const toggleAudio = () => {
    if (isPlaying) {
      speechSynthesis.pause();
      setIsPlaying(false);
    } else {
      // Resume if paused, or start new synthesis
      if (speechSynthesis.paused) {
        speechSynthesis.resume();
        setIsPlaying(true);
      } else {
        // If there's a current synthesis text, speak it
        if (synthesisText) {
          handleVoiceSynthesis(synthesisText);
        } else {
          // Find the latest AI response from conversation history
          const latestAIResponse = conversationHistory
            .filter(msg => msg.speaker === 'ai')
            .pop();
          
          if (latestAIResponse) {
            handleVoiceSynthesis(latestAIResponse.text);
          } else {
            toast({
              title: "🔇 No Audio",
              description: "No AI response to speak",
              variant: "destructive"
            });
          }
        }
      }
    }
  };

  // Stop audio
  const stopAudio = () => {
    speechSynthesis.cancel();
    setIsAISpeaking(false);
    setIsPlaying(false);
  };

  // Initialize speech recognition
  const initializeSpeechRecognition = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = true;
      recognition.lang = 'en-US';
      
      recognition.onstart = () => {
        setIsListening(true);
        setRecognizedText("");
        toast({
          title: "🎤 Listening...",
          description: "Speak your question or request",
          duration: 2000
        });
      };
      
      recognition.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        const currentText = finalTranscript || interimTranscript;
        setRecognizedText(currentText);
        
        // Store the final transcript for use in onend
        if (finalTranscript) {
          finalTranscriptRef.current = finalTranscript;
        }
      };
      
      recognition.onend = () => {
        setIsListening(false);
        const finalText = finalTranscriptRef.current || recognizedText;
        console.log('🎤 Speech recognition ended. Final text:', finalText);
        if (finalText && finalText.trim()) {
          handleVoiceInput(finalText);
        } else {
          console.log('❌ No speech detected');
          toast({
            title: "🔇 No Speech Detected",
            description: "Please try speaking again",
            variant: "destructive"
          });
        }
      };
      
      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        toast({
          title: "❌ Speech Recognition Error",
          description: `Error: ${event.error}`,
          variant: "destructive"
        });
      };
      
      recognitionRef.current = recognition;
      return recognition;
    }
    return null;
  };

  // Handle voice input and AI response
  const handleVoiceInput = async (text: string) => {
    if (!text.trim()) {
      console.log('❌ Empty voice input received');
      return;
    }
    
    console.log('🎤 Voice input received:', text);
    
    // Add user message to conversation
    setConversationHistory(prev => [...prev, { speaker: 'user', text }]);
    
    setIsProcessing(true);
    
    try {
      console.log('🔄 Getting AI response from backend...');
      // Try to get AI response from backend first
      let aiResponse = await getAIResponseFromBackend(text);
      
      // Fallback to mock response if backend fails
      if (!aiResponse) {
        console.log('⚠️ Backend failed, using mock response');
        aiResponse = await generateAIResponse(text);
      }
      
      console.log('🤖 AI Response received:', aiResponse);
      
      // Add AI response to conversation
      setConversationHistory(prev => [...prev, { speaker: 'ai', text: aiResponse }]);
      
      // Speak the AI response
      console.log('🔊 Starting voice synthesis for:', aiResponse);
      await handleVoiceSynthesis(aiResponse);
      
    } catch (error) {
      console.error('❌ AI response error:', error);
      toast({
        title: "❌ AI Error",
        description: "Failed to get AI response",
        variant: "destructive"
      });
    } finally {
      setIsProcessing(false);
    }
  };

  // Get AI response from backend
  const getAIResponseFromBackend = async (text: string): Promise<string | null> => {
    try {
      console.log('🎤 Sending voice input to backend:', text);
      
      // Use the main chat endpoint which handles all types of queries
      const response = await apiClient.sendChatMessage(text, 'en');
      
      if (response.success && response.data) {
        console.log('✅ Backend response received:', response.data.response);
        return response.data.response;
      } else {
        console.log('❌ Backend response failed:', response.error);
        return null;
      }
    } catch (error) {
      console.error('❌ Backend API error:', error);
      return null;
    }
  };

  // Generate AI response (mock implementation)
  const generateAIResponse = async (userInput: string): Promise<string> => {
    // Mock AI responses based on input
    const responses = {
      'hello': "Hello! I'm your MoneyLingo financial assistant. How can I help you today?",
      'help': "I can help you with budgeting, saving, investing, credit management, and financial planning. What would you like to know?",
      'budget': "Let me help you create a budget. First, tell me about your monthly income and expenses.",
      'save': "Great! Let's talk about saving strategies. What's your current financial goal?",
      'invest': "Investing can help grow your wealth over time. What's your investment timeline and risk tolerance?",
      'credit': "Credit management is crucial for financial health. I can help you understand credit scores, building credit, and managing debt.",
      'debt': "Let's tackle your debt together. What types of debt do you have and what are the interest rates?",
      'retirement': "Planning for retirement is important at any age. Let's discuss your retirement goals and timeline.",
      'tax': "Tax planning can save you money. I can help you understand deductions, credits, and tax-advantaged accounts."
    };
    
    const lowerInput = userInput.toLowerCase();
    
    for (const [keyword, response] of Object.entries(responses)) {
      if (lowerInput.includes(keyword)) {
        return response;
      }
    }
    
    return `I understand you're asking about "${userInput}". As your financial assistant, I'm here to help with budgeting, saving, investing, credit, and financial planning. Could you be more specific about what you'd like to know?`;
  };

  // Start listening
  const startListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.start();
    } else {
      const recognition = initializeSpeechRecognition();
      if (recognition) {
        recognition.start();
      } else {
        toast({
          title: "❌ Speech Recognition Not Supported",
          description: "Your browser doesn't support speech recognition",
          variant: "destructive"
        });
      }
    }
  };

  // Stop listening
  const stopListening = () => {
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    setIsListening(false);
  };

  // Simulate microphone input and AI speaking
  useEffect(() => {
    if (!isActive) return;

    const interval = setInterval(() => {
      // Simulate audio levels - very slow updates for calming effect
      if (isAISpeaking) {
        setAudioLevel(Math.random() * 100);
      } else if (!isMuted) {
        setAudioLevel(Math.random() * 80);
      } else {
        setAudioLevel(0);
      }
    }, 600); // Much slower update rate

    // Simulate AI speaking randomly (demo mode)
    const aiSpeakInterval = setInterval(() => {
      if (!isProcessing) {
        setIsAISpeaking((prev) => !prev);
      }
    }, 4000);

    return () => {
      clearInterval(interval);
      clearInterval(aiSpeakInterval);
    };
  }, [isActive, isMuted, isAISpeaking, isProcessing]);

  // Cleanup audio on unmount
  useEffect(() => {
    return () => {
      // Stop any ongoing speech synthesis
      speechSynthesis.cancel();
      setIsAISpeaking(false);
      setIsPlaying(false);
    };
  }, []);

  if (!isActive) return null;

  const circleScale = 1 + (audioLevel / 100) * 0.15; // Even more reduced scale range

  return (
    <div className="fixed inset-0 z-50 bg-gradient-soft-bg animate-fade-in overflow-hidden">
      {/* Floating decorative elements */}
      <div className="absolute top-20 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <div className="relative h-full flex flex-col items-center justify-between py-12 px-4 sm:px-6 gap-8">
        {/* Status indicator */}
        <div className="text-center animate-fade-in-up flex-shrink-0">
          <div className="glass-card px-6 py-3 rounded-full inline-flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full animate-pulse ${
              isListening ? 'bg-green-500' : 
              isProcessing ? 'bg-yellow-500' : 
              isAISpeaking ? 'bg-blue-500' : 'bg-primary'
            }`} />
            <span className="text-base text-foreground font-medium">
              {isListening ? "Listening..." : 
               isProcessing ? "Processing..." : 
               isAISpeaking ? "AI is speaking..." : 
               "Ready to listen"}
            </span>
          </div>
        </div>

        {/* Recognized text display */}
        {recognizedText && (
          <div className="text-center animate-fade-in-up">
            <div className="glass-card px-6 py-3 rounded-2xl inline-block max-w-md">
              <p className="text-sm text-muted-foreground mb-1">You said:</p>
              <p className="text-base text-foreground font-medium">{recognizedText}</p>
            </div>
          </div>
        )}

        {/* Main sound wave circle - centered with proper spacing */}
        <div className="relative flex items-center justify-center flex-1 max-h-[450px]">
          {/* Outer rings with glass effect */}
          {[...Array(3)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full bg-primary/10 backdrop-blur-sm"
              style={{
                width: `${220 + i * 70}px`,
                height: `${220 + i * 70}px`,
                animation: `ping ${4 + i * 2}s cubic-bezier(0.4, 0, 0.6, 1) infinite`,
                animationDelay: `${i * 0.7}s`,
                opacity: audioLevel > 10 ? 0.4 - i * 0.1 : 0.1,
              }}
            />
          ))}

          {/* Main circle with dynamic gradient using design system */}
          <div
            className="relative z-10 rounded-full shadow-2xl ease-out glow-pulse"
            style={{
              width: "220px",
              height: "220px",
              transform: `scale(${circleScale})`,
              background: `linear-gradient(${audioLevel * 1.2}deg, hsl(180, 62%, ${35 + audioLevel / 8}%), hsl(192, 81%, ${50 + audioLevel / 12}%), hsl(25, 95%, ${63 + audioLevel / 15}%))`,
              transition: "all 1200ms cubic-bezier(0.4, 0, 0.2, 1)",
            }}
          >
          </div>
        </div>

        {/* Bottom section with buttons and info */}
        <div className="flex flex-col items-center gap-6 w-full flex-shrink-0">
          {/* Call info */}
          <div className="text-center animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
            <p className="text-xl font-semibold mb-2">
              <span className="shimmer-text">Voice call active</span>
            </p>
            <p className="text-base text-muted-foreground">
              Ask me anything about finance
            </p>
          </div>

          {/* Control buttons */}
          <div className="flex items-center gap-4 sm:gap-6 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
            <Button
              size="icon"
              variant={isListening ? "default" : "secondary"}
              onClick={isListening ? stopListening : startListening}
              disabled={isProcessing}
              className={`h-14 w-14 sm:h-16 sm:w-16 rounded-full shadow-xl hover-lift transition-all duration-300 ${
                isListening ? 'bg-primary animate-pulse' : 'bg-secondary'
              }`}
              aria-label={isListening ? "Stop listening" : "Start listening"}
            >
              {isListening ? <MicOff className="h-6 w-6 sm:h-8 sm:w-8" /> : <Mic className="h-6 w-6 sm:h-8 sm:w-8" />}
            </Button>

            <Button
              size="icon"
              onClick={() => handleVoiceSynthesis("Hello! I'm your financial assistant. How can I help you today?")}
              disabled={isProcessing}
              className="h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-primary hover:bg-primary/90 shadow-xl hover-lift transition-all duration-300"
              aria-label="Test voice synthesis"
            >
              <Volume2 className="h-6 w-6 sm:h-8 sm:w-8" />
            </Button>

            {(synthesisText || conversationHistory.some(msg => msg.speaker === 'ai')) && (
              <>
                <Button
                  size="icon"
                  onClick={toggleAudio}
                  disabled={isProcessing}
                  className="h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-accent hover:bg-accent/90 shadow-xl hover-lift transition-all duration-300"
                  aria-label={isPlaying ? "Pause audio" : "Play audio"}
                >
                  {isPlaying ? <Pause className="h-6 w-6 sm:h-8 sm:w-8" /> : <Play className="h-6 w-6 sm:h-8 sm:w-8" />}
                </Button>

                <Button
                  size="icon"
                  onClick={stopAudio}
                  className="h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-secondary hover:bg-secondary/90 shadow-xl hover-lift transition-all duration-300"
                  aria-label="Stop audio"
                >
                  <Volume2 className="h-6 w-6 sm:h-8 sm:w-8" />
                </Button>
              </>
            )}

            <Button
              size="icon"
              onClick={onEnd}
              className="h-14 w-14 sm:h-16 sm:w-16 rounded-full bg-destructive hover:bg-destructive/90 shadow-2xl hover-lift transition-all duration-300 glow-pulse no-underline"
              aria-label="End call"
            >
              <PhoneOff className="h-6 w-6 sm:h-8 sm:w-8 no-underline" style={{ textDecoration: 'none' }} />
            </Button>
          </div>

          {/* Conversation Display */}
          {conversationHistory.length > 0 && (
            <div className="w-full max-w-2xl animate-fade-in-up" style={{ animationDelay: "0.4s" }}>
              <div className="glass-card p-4 rounded-2xl max-h-48 overflow-y-auto">
                <div className="space-y-3">
                  {conversationHistory.map((message, index) => (
                    <div
                      key={index}
                      className={`flex ${message.speaker === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xs px-4 py-2 rounded-2xl ${
                          message.speaker === 'user'
                            ? 'bg-primary text-primary-foreground'
                            : 'bg-secondary text-secondary-foreground'
                        }`}
                      >
                        <div className="flex items-center gap-2 mb-1">
                          <MessageSquare className="h-4 w-4" />
                          <span className="text-xs font-medium">
                            {message.speaker === 'user' ? 'You' : 'AI Assistant'}
                          </span>
                        </div>
                        <p className="text-sm">{message.text}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Voice synthesis input */}
          <div className="w-full max-w-md animate-fade-in-up" style={{ animationDelay: "0.5s" }}>
            <div className="glass-card p-4 rounded-2xl">
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Type text to synthesize..."
                  value={synthesisText}
                  onChange={(e) => setSynthesisText(e.target.value)}
                  className="flex-1 px-4 py-2 bg-background/50 border border-border/50 rounded-xl text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary/50 transition-all duration-200"
                />
                <Button
                  onClick={() => handleVoiceSynthesis(synthesisText)}
                  disabled={!synthesisText.trim() || isProcessing}
                  className="px-4 py-2 bg-primary hover:bg-primary/90 rounded-xl"
                >
                  {isProcessing ? "..." : "Speak"}
                </Button>
              </div>
            </div>
          </div>

          {/* Tips */}
          <div className="glass-card px-8 py-3 rounded-full text-center animate-fade-in-up inline-block" style={{ animationDelay: "0.5s" }}>
            <p className="text-sm text-muted-foreground whitespace-nowrap">
              💡 Speak naturally about credit, taxes, mortgages, or any financial topic
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
