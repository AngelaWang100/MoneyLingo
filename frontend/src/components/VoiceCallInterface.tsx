import { Button } from "@/components/ui/button";
import { PhoneOff, Mic, MicOff, Volume2 } from "lucide-react";
import { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";

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

  // Handle voice synthesis and audio playback
  const handleVoiceSynthesis = async (text: string) => {
    if (!text.trim()) return;
    
    setIsProcessing(true);
    try {
      const response = await apiClient.synthesizeVoice({
        text,
        language: 'en',
        voice_id: '21m00Tcm4TlvDq8ikWAM'
      });
      
      if (response.success && response.data?.audio_url) {
        // Stop any current audio
        if (currentAudio) {
          currentAudio.pause();
          currentAudio.currentTime = 0;
        }
        
        // Play new audio
        const audio = new Audio(response.data.audio_url);
        setCurrentAudio(audio);
        
        audio.onplay = () => setIsAISpeaking(true);
        audio.onended = () => setIsAISpeaking(false);
        audio.onerror = () => setIsAISpeaking(false);
        
        await audio.play();
      }
    } catch (error) {
      console.error('Voice synthesis error:', error);
    } finally {
      setIsProcessing(false);
    }
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
      if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
      }
    };
  }, [currentAudio]);

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
            <div className="w-3 h-3 bg-primary rounded-full animate-pulse" />
            <span className="text-base text-foreground font-medium">
              {isProcessing ? "Processing..." : isAISpeaking ? "AI is speaking..." : "Listening..."}
            </span>
          </div>
        </div>

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
          <div className="flex items-center gap-6 sm:gap-8 animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
            <Button
              size="icon"
              variant={isMuted ? "destructive" : "secondary"}
              onClick={() => setIsMuted(!isMuted)}
              className="h-16 w-16 sm:h-20 sm:w-20 rounded-full shadow-xl hover-lift transition-all duration-300"
              aria-label={isMuted ? "Unmute" : "Mute"}
            >
              {isMuted ? <MicOff className="h-8 w-8 sm:h-10 sm:w-10" /> : <Mic className="h-8 w-8 sm:h-10 sm:w-10" />}
            </Button>

            <Button
              size="icon"
              onClick={() => handleVoiceSynthesis("Hello! I'm your financial assistant. How can I help you today?")}
              disabled={isProcessing}
              className="h-16 w-16 sm:h-20 sm:w-20 rounded-full bg-primary hover:bg-primary/90 shadow-xl hover-lift transition-all duration-300"
              aria-label="Test voice synthesis"
            >
              <Volume2 className="h-8 w-8 sm:h-10 sm:w-10" />
            </Button>

            <Button
              size="icon"
              onClick={onEnd}
              className="h-16 w-16 sm:h-20 sm:w-20 rounded-full bg-destructive hover:bg-destructive/90 shadow-2xl hover-lift transition-all duration-300 glow-pulse no-underline"
              aria-label="End call"
            >
              <PhoneOff className="h-8 w-8 sm:h-10 sm:w-10 no-underline" style={{ textDecoration: 'none' }} />
            </Button>
          </div>

          {/* Tips */}
          <div className="glass-card px-8 py-3 rounded-full text-center animate-fade-in-up inline-block" style={{ animationDelay: "0.4s" }}>
            <p className="text-sm text-muted-foreground whitespace-nowrap">
              💡 Speak naturally about credit, taxes, mortgages, or any financial topic
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
