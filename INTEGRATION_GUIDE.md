# 🚀 MoneyLingo Frontend-Backend Integration Guide

## 📋 Overview

This guide explains how to integrate your React frontend with the MoneyLingo FastAPI backend. The integration provides:

- **Real-time Chat**: AI-powered financial conversations
- **Voice Synthesis**: ElevenLabs voice responses
- **Translation**: Multi-language support
- **Financial Planning**: AI financial advice
- **Remittance Analysis**: XRPL blockchain integration

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   React Frontend │ ◄─────────────────► │  FastAPI Backend │
│   (Port 3000)   │                      │   (Port 8001)   │
└─────────────────┘                      └─────────────────┘
         │                                        │
         │                                        │
         ▼                                        ▼
┌─────────────────┐                      ┌─────────────────┐
│   UI Components │                      │   AI Agents    │
│   - Chat        │                      │   - Translation │
│   - Voice       │                      │   - Financial   │
│   - Auth        │                      │   - Remittance  │
└─────────────────┘                      └─────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Backend dependencies (already installed)
pip install -r requirements.txt

# Frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Environment Setup

Create `.env` file in the root directory:

```bash
# Backend Environment Variables
GOOGLE_API_KEY=your_google_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
COMET_API_KEY=your_comet_api_key
COMET_WORKSPACE=your_workspace
XRPL_TESTNET_URL=https://s.altnet.rippletest.net:51234

# Database (if using)
DATABASE_URL=sqlite:///./realitycheck.db
```

Create `frontend/.env.local`:

```bash
# Frontend Environment Variables
VITE_API_URL=http://localhost:8001
VITE_DEV_MODE=true
VITE_DEBUG_API=false
VITE_DEFAULT_VOICE_ID=21m00Tcm4TlvDq8ikWAM
VITE_VOICE_ENABLED=true
```

### 3. Start Development Servers

**Option A: Use the startup script (Recommended)**
```bash
./start_dev.sh
```

**Option B: Manual startup**
```bash
# Terminal 1: Backend
python main_new.py

# Terminal 2: Frontend
cd frontend
npm run dev
```

## 🔌 API Integration

### Chat Integration

The frontend now connects to your backend chat API:

```typescript
// Frontend API call
const response = await apiClient.sendChatMessage(message, language);

// Backend endpoint
POST /api/v1/financial/chat
{
  "question": "How do I save for retirement?",
  "language": "en",
  "user_level": "beginner"
}
```

### Voice Integration

Voice synthesis is integrated with ElevenLabs:

```typescript
// Frontend voice synthesis
const response = await apiClient.synthesizeVoice({
  text: "Hello! I'm your financial assistant.",
  language: "en",
  voice_id: "21m00Tcm4TlvDq8ikWAM"
});

// Backend endpoint
POST /api/v1/voice/synthesize
{
  "text": "Hello! I'm your financial assistant.",
  "language": "en",
  "voice_id": "21m00Tcm4TlvDq8ikWAM"
}
```

### Translation Integration

Multi-language support:

```typescript
// Frontend translation
const response = await apiClient.translateText({
  text: "How do I invest my money?",
  target_language: "es",
  source_language: "en"
});

// Backend endpoint
POST /api/v1/translate
{
  "text": "How do I invest my money?",
  "target_language": "es",
  "source_language": "en"
}
```

## 🎯 Available Endpoints

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/financial/chat` | POST | AI chat responses |
| `/api/v1/financial/advice` | POST | Financial planning advice |
| `/api/v1/voice/synthesize` | POST | Voice synthesis |
| `/api/v1/translate` | POST | Text translation |
| `/api/v1/remittance/analyze` | POST | Remittance analysis |
| `/api/v1/monetization/*` | POST | Echo AI monetization |

### Frontend Routes

| Route | Component | Description |
|-------|-----------|-------------|
| `/` | Index | Landing page |
| `/chat` | Chat | AI conversation interface |
| `/dashboard` | Dashboard | User dashboard |
| `/signin` | SignIn | Authentication |
| `/signup` | SignUp | User registration |

## 🔧 Configuration

### CORS Settings

The backend is configured to allow all origins in development:

```python
# main_new.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API Client Configuration

The frontend API client is configured in `frontend/src/lib/api.ts`:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
```

## 🧪 Testing the Integration

### 1. Health Check
```bash
curl http://localhost:8001/health
```

### 2. Chat API
```bash
curl -X POST http://localhost:8001/api/v1/financial/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How do I save money?", "language": "en"}'
```

### 3. Voice API
```bash
curl -X POST http://localhost:8001/api/v1/voice/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "language": "en"}'
```

## 🚀 Deployment

### Frontend Deployment (Vercel)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy automatically on push

### Backend Deployment

1. Deploy to your preferred platform (Railway, Render, etc.)
2. Set environment variables
3. Update `VITE_API_URL` in frontend to production URL

## 🔍 Troubleshooting

### Common Issues

1. **CORS Errors**: Ensure backend CORS is configured correctly
2. **API Connection**: Check that `VITE_API_URL` is correct
3. **Voice Issues**: Verify ElevenLabs API key is set
4. **Translation**: Ensure Google API key is configured

### Debug Mode

Enable debug mode in frontend:
```bash
VITE_DEBUG_API=true
```

This will log all API requests to the console.

## 📱 Features

### ✅ Implemented
- [x] Chat interface with backend integration
- [x] Voice synthesis with ElevenLabs
- [x] Multi-language support
- [x] Error handling and fallbacks
- [x] Loading states and user feedback
- [x] CORS configuration
- [x] Development startup script

### 🚧 In Progress
- [ ] Authentication integration
- [ ] Real-time voice input
- [ ] File upload for documents
- [ ] User session management

### 📋 Planned
- [ ] WebSocket for real-time chat
- [ ] Push notifications
- [ ] Offline mode
- [ ] Progressive Web App features

## 🎉 Success!

Your frontend and backend are now integrated! You can:

1. **Chat with AI**: Send messages and get financial advice
2. **Voice Synthesis**: Hear AI responses in natural voice
3. **Multi-language**: Get responses in different languages
4. **Financial Planning**: Get personalized financial advice
5. **Remittance Analysis**: Analyze international transfers

Visit `http://localhost:3000` to see your integrated application!
