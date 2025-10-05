import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Input } from "@/components/ui/input";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { VoiceCallInterface } from "@/components/VoiceCallInterface";
import { useState, useEffect } from "react";
import { Upload, FileText, Search, Shield, Trash2, Eye, Lock, Phone, Headphones } from "lucide-react";
import { Link } from "react-router-dom";

const Documents = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isCallActive, setIsCallActive] = useState(false);

  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated") === "true";
    setIsAuthenticated(authStatus);
  }, []);
  const [searchQuery, setSearchQuery] = useState("");

  const documents = [
    { id: 1, name: "Tax Return 2023.pdf", type: "Tax Form", date: "Jan 15, 2024", status: "analyzed" },
    { id: 2, name: "Credit Card Statement.pdf", type: "Credit Statement", date: "Jan 10, 2024", status: "analyzed" },
    { id: 3, name: "Bank Statement Dec.pdf", type: "Bank Statement", date: "Jan 5, 2024", status: "pending" },
  ];

  const filteredDocs = documents.filter((doc) =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Main Gradient Background */}
      <div className="fixed inset-0 bg-gradient-main pointer-events-none" />
      
      {/* Cloud-like soft shapes */}
      <div className="fixed inset-0 bg-gradient-clouds pointer-events-none" />
      
      {/* Subtle overlay for depth */}
      <div className="fixed inset-0 bg-gradient-to-b from-transparent via-background/5 to-background/20 pointer-events-none" />
      
      <Header />

      <main className="flex-1 container mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 relative z-10">
        <div className="mb-6 sm:mb-8 animate-fade-in-up px-4 sm:px-0">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold shimmer-text mb-2 leading-tight">Document Analysis</h1>
          <p className="text-sm sm:text-base text-muted-foreground mb-6">
            Upload your financial documents for AI-powered explanations in your language.
          </p>
          
          {/* Prominent Call Button */}
          <div className="flex flex-col sm:flex-row items-center gap-3" style={{ animationDelay: "0.2s" }}>
            <Button
              onClick={() => setIsCallActive(true)}
              size="lg"
              className="h-14 px-8 bg-gradient-glow text-white rounded-full hover:scale-105 transition-all duration-300 shadow-2xl glow-pulse text-base font-semibold"
            >
              <Phone className="h-5 w-5 mr-2 animate-pulse" />
              Talk to AI Assistant
            </Button>
            <p className="text-xs text-muted-foreground flex items-center gap-1.5">
              <Headphones className="h-3.5 w-3.5" />
              Get instant help analyzing your documents
            </p>
          </div>
        </div>

        {/* Auth Alert */}
        {!isAuthenticated && (
          <Alert className="mb-4 sm:mb-6 border-primary/50 bg-primary/5 animate-fade-in">
            <Lock className="h-4 w-4 text-primary" />
            <AlertDescription className="flex flex-col sm:flex-row items-start sm:items-center gap-3 sm:justify-between">
              <span className="text-sm">Sign in to upload and analyze your financial documents securely.</span>
              <div className="flex gap-2 w-full sm:w-auto sm:ml-4">
                <Button size="sm" asChild className="flex-1 sm:flex-initial hover-lift">
                  <Link to="/signin">Sign In</Link>
                </Button>
                <Button size="sm" variant="outline" asChild className="flex-1 sm:flex-initial hover-lift">
                  <Link to="/signup">Sign Up</Link>
                </Button>
              </div>
            </AlertDescription>
          </Alert>
        )}

        {/* Upload Section */}
        <Card className={`mb-6 sm:mb-8 border-2 border-dashed transition-all glass-card animate-fade-in-up ${!isAuthenticated ? 'opacity-60' : 'hover:border-primary/50 hover-card-lift'}`} style={{ animationDelay: "0.1s" }}>
          <CardContent className="p-8 sm:p-12">
            <div className="text-center space-y-4">
              <div className="mx-auto h-16 w-16 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg">
                <Upload className="h-8 w-8 text-primary-foreground" aria-hidden="true" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">Upload Your Documents</h3>
                <p className="text-sm sm:text-base text-muted-foreground mb-4">
                  {isAuthenticated ? 'Drag and drop files here, or click to browse' : 'Sign in to upload documents'}
                </p>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  Supported formats: PDF, JPG, PNG (Max 10MB)
                </p>
              </div>
              <Button size="lg" className="mt-4 bg-gradient-primary hover:scale-105 transition-all duration-300 shadow-lg" disabled={!isAuthenticated}>
                <Upload className="mr-2 h-5 w-5" />
                Choose Files
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Security Notice */}
        <Card className="mb-6 sm:mb-8 border-primary/20 glass-card animate-fade-in-up" style={{ animationDelay: "0.2s" }}>
          <CardContent className="p-4 sm:p-6">
            <div className="flex items-start gap-4">
              <div className="h-10 w-10 rounded-xl bg-gradient-primary flex items-center justify-center flex-shrink-0 shadow-lg">
                <Shield className="h-5 w-5 text-primary-foreground" />
              </div>
              <div>
                <h3 className="font-semibold mb-1 text-sm sm:text-base">Your Documents Are Secure</h3>
                <p className="text-xs sm:text-sm text-muted-foreground">
                  All documents are encrypted end-to-end and stored with bank-level security. We never share your financial information with third parties.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Document List */}
        <div className="animate-fade-in-up" style={{ animationDelay: "0.3s" }}>
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4 sm:mb-6 px-4 sm:px-0">
            <h2 className="text-xl sm:text-2xl font-bold shimmer-text">Your Documents</h2>
            <div className="relative w-full sm:max-w-sm">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search documents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
                aria-label="Search documents"
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-3 sm:gap-4">
            {filteredDocs.map((doc, index) => (
              <Card key={doc.id} className="hover:border-primary/50 transition-all glass-card hover-card-lift animate-fade-in-up" style={{ animationDelay: `${0.4 + index * 0.1}s` }}>
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="h-12 w-12 rounded-xl bg-gradient-primary flex items-center justify-center shadow-lg">
                      <FileText className="h-6 w-6 text-primary-foreground" />
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        doc.status === "analyzed"
                          ? "bg-primary/10 text-primary"
                          : "bg-muted text-muted-foreground"
                      }`}
                    >
                      {doc.status === "analyzed" ? "Analyzed" : "Pending"}
                    </span>
                  </div>
                  <CardTitle className="text-base mt-4 truncate">{doc.name}</CardTitle>
                  <CardDescription>
                    <span className="block text-sm">{doc.type}</span>
                    <span className="block text-xs mt-1">{doc.date}</span>
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex gap-2">
                    <Button size="sm" variant="outline" className="flex-1 hover-card-lift" disabled={!isAuthenticated}>
                      <Eye className="mr-2 h-4 w-4" />
                      View
                    </Button>
                    <Button size="sm" variant="ghost" className="hover-card-lift" disabled={!isAuthenticated}>
                      <Trash2 className="h-4 w-4 text-destructive" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {filteredDocs.length === 0 && (
            <Card className="p-8 sm:p-12 glass-card">
              <div className="text-center text-muted-foreground">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-sm sm:text-base">No documents found matching your search.</p>
              </div>
            </Card>
          )}
        </div>
      </main>

      <Footer />
      
      {/* Voice Call Interface */}
      <VoiceCallInterface 
        isActive={isCallActive}
        onEnd={() => setIsCallActive(false)}
      />
    </div>
  );
};

export default Documents;
