import { Link } from "react-router-dom";
import { Facebook, Twitter, Linkedin, Mail } from "lucide-react";

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t bg-gradient-to-br from-slate-900 to-slate-800 text-slate-100">
      <div className="container mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-4">
            <div className="flex items-center gap-2 text-xl font-bold text-white">
              <span className="text-2xl" aria-hidden="true">💰</span>
              <span>MoneyLingo</span>
            </div>
            <p className="text-sm text-slate-300">
              Breaking down barriers in finance through language and accessibility.
            </p>
            <div className="flex gap-4">
              <a href="#" className="text-slate-300 hover:text-white transition-colors" aria-label="Facebook">
                <Facebook className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-300 hover:text-white transition-colors" aria-label="Twitter">
                <Twitter className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-300 hover:text-white transition-colors" aria-label="LinkedIn">
                <Linkedin className="h-5 w-5" />
              </a>
              <a href="#" className="text-slate-300 hover:text-white transition-colors" aria-label="Email">
                <Mail className="h-5 w-5" />
              </a>
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-4 text-white">Product</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/chat" className="text-slate-300 hover:text-white transition-colors">
                  AI Chat
                </Link>
              </li>
              <li>
                <Link to="/documents" className="text-slate-300 hover:text-white transition-colors">
                  Document Analysis
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-slate-300 hover:text-white transition-colors">
                  Dashboard
                </Link>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4 text-white">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-slate-300 hover:text-white transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <a href="#faq" className="text-slate-300 hover:text-white transition-colors">
                  FAQ
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Blog
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold mb-4 text-white">Legal</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Terms of Service
                </a>
              </li>
              <li>
                <a href="#" className="text-slate-300 hover:text-white transition-colors">
                  Security
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-slate-700 text-center text-sm text-slate-300">
          <p>&copy; {currentYear} MoneyLingo. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};
