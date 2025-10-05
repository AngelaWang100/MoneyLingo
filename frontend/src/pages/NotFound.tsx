import { Link, useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Home, MessageSquare } from "lucide-react";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute inset-0 bg-gradient-soft-bg pointer-events-none" />
      <div className="absolute top-20 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <div className="text-center relative z-10 px-4 glass-card p-12 rounded-3xl max-w-lg mx-4 animate-fade-in-up">
        <div className="text-8xl font-bold shimmer-text mb-4">404</div>
        <h1 className="mb-4 text-2xl md:text-3xl font-bold">Oops! Page not found</h1>
        <p className="mb-8 text-lg text-muted-foreground">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button asChild size="lg" className="bg-gradient-primary hover:scale-105 transition-all duration-300 shadow-lg">
            <Link to="/">
              <Home className="mr-2 h-5 w-5" />
              Return to Home
            </Link>
          </Button>
          <Button asChild size="lg" variant="outline" className="hover-card-lift">
            <Link to="/chat">
              <MessageSquare className="mr-2 h-5 w-5" />
              Chat with AI
            </Link>
          </Button>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
