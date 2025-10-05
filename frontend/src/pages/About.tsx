import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { Link } from "react-router-dom";
import { Heart, Users, Target, Shield } from "lucide-react";

const About = () => {
  const values = [
    {
      icon: Heart,
      title: "Empathy First",
      description: "We understand the challenges immigrants and ESL speakers face in navigating complex financial systems.",
    },
    {
      icon: Users,
      title: "Cultural Inclusivity",
      description: "Financial advice that respects and incorporates diverse cultural perspectives and experiences.",
    },
    {
      icon: Target,
      title: "Clear Communication",
      description: "Breaking down complex financial jargon into simple, accessible language everyone can understand.",
    },
    {
      icon: Shield,
      title: "Trust & Security",
      description: "Your financial information is protected with the highest security standards in the industry.",
    },
  ];

  return (
    <div className="min-h-screen flex flex-col relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute inset-0 bg-gradient-soft-bg pointer-events-none" />
      <div className="absolute top-20 right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-float pointer-events-none" />
      <div className="absolute bottom-20 left-10 w-96 h-96 bg-accent/10 rounded-full blur-3xl animate-pulse-slow pointer-events-none" />
      
      <Header />

      <main className="flex-1 relative z-10">
        {/* Hero Section */}
        <section className="py-20 animate-fade-in-up">
          <div className="container mx-auto px-4 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 shimmer-text">
              Breaking Down Financial Barriers
            </h1>
            <p className="text-xl max-w-3xl mx-auto text-muted-foreground">
              MoneyLingo was created to make financial literacy accessible to everyone, regardless of language or background.
            </p>
          </div>
        </section>

        {/* Mission Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl md:text-4xl font-bold text-center mb-8">Our Mission</h2>
              <p className="text-lg text-muted-foreground text-center mb-12">
                We believe financial literacy should not be limited by language barriers or cultural unfamiliarity with the American financial system. Our mission is to empower immigrants and ESL speakers with the knowledge and tools they need to achieve financial success.
              </p>

              <div className="grid md:grid-cols-2 gap-8">
                <Card className="glass-card hover-card-lift">
                  <CardContent className="p-8">
                    <h3 className="text-2xl font-bold mb-4">The Problem</h3>
                    <p className="text-muted-foreground">
                      Millions of immigrants and ESL speakers struggle to understand financial documents, credit systems, and tax requirements in their non-native language. This creates barriers to financial security and opportunity.
                    </p>
                  </CardContent>
                </Card>

                <Card className="glass-card hover-card-lift">
                  <CardContent className="p-8">
                    <h3 className="text-2xl font-bold mb-4">Our Solution</h3>
                    <p className="text-muted-foreground">
                      AI-powered financial guidance in your native language, with culturally-aware explanations and personalized support that makes complex financial concepts accessible to everyone.
                    </p>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </section>

        {/* Values Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl md:text-4xl font-bold text-center mb-4">Our Values</h2>
            <p className="text-lg text-muted-foreground text-center mb-12 max-w-2xl mx-auto">
              These principles guide everything we do at MoneyLingo
            </p>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
              {values.map((value, index) => {
                const Icon = value.icon;
                return (
                  <Card key={value.title} className="text-center glass-card hover-card-lift animate-fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                    <CardContent className="p-6">
                      <div className="h-16 w-16 rounded-full bg-gradient-primary flex items-center justify-center mx-auto mb-4 shadow-lg">
                        <Icon className="h-8 w-8 text-primary-foreground" aria-hidden="true" />
                      </div>
                      <h3 className="text-xl font-bold mb-2">{value.title}</h3>
                      <p className="text-sm text-muted-foreground">{value.description}</p>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          </div>
        </section>

        {/* Impact Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center">
              <h2 className="text-3xl md:text-4xl font-bold mb-8">Making an Impact</h2>
              <div className="grid md:grid-cols-3 gap-8 mb-12">
                <div>
                  <p className="text-5xl font-bold text-primary mb-2">10K+</p>
                  <p className="text-muted-foreground">Users Served</p>
                </div>
                <div>
                  <p className="text-5xl font-bold text-primary mb-2">25+</p>
                  <p className="text-muted-foreground">Languages Supported</p>
                </div>
                <div>
                  <p className="text-5xl font-bold text-primary mb-2">50K+</p>
                  <p className="text-muted-foreground">Documents Analyzed</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="container mx-auto px-4">
            <div className="max-w-4xl mx-auto text-center glass-card p-8 sm:p-12 rounded-3xl">
              <h2 className="text-3xl md:text-4xl font-bold mb-4 shimmer-text">
                Join Us in Breaking Down Barriers
              </h2>
              <p className="text-xl mb-8 text-muted-foreground max-w-2xl mx-auto">
                Start your journey to financial confidence today, in your own language.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button size="lg" asChild className="bg-gradient-primary hover:scale-105 transition-all duration-300 shadow-lg">
                  <Link to="/signup">Get Started</Link>
                </Button>
                <Button size="lg" variant="outline" asChild className="hover-card-lift">
                  <Link to="/#faq">View FAQ</Link>
                </Button>
              </div>
            </div>
          </div>
        </section>
      </main>

      <Footer />
    </div>
  );
};

export default About;
