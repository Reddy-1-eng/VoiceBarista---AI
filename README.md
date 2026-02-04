# ☕ AgentX Coffee Shop - AI Voice Barista

> **AgentX - Agentic Development Competition 2026**  
> **Woxsen University, Hyderabad**  
> **Team Size: 5 Members**

[![LiveKit](https://img.shields.io/badge/Built%20with-LiveKit-00ADD8?logo=livekit)](https://livekit.io/)
[![Google AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4?logo=google)](https://ai.google.dev/)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-000000?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Backend-Python%203.9+-3776AB?logo=python)](https://python.org/)

## 🎯 **Competition Overview**

**AgentX Coffee Shop** is an autonomous AI voice barista system that demonstrates independent decision-making, adaptability, and real-world relevance. Built for the AgentX - Agentic Development Competition, this project showcases cutting-edge voice AI technology in a practical business application.

### **🏆 Competition Criteria Met:**
- ✅ **Innovation & Originality** - Real-time voice AI with visual feedback
- ✅ **Autonomous Decision-Making** - Independent order validation and management
- ✅ **Adaptability** - Dynamic conversation flow based on user input
- ✅ **Real-World Relevance** - Practical solution for coffee shops and restaurants
- ✅ **Technical Excellence** - Modern tech stack with production-ready architecture

## 🚀 **Key Features**

### **🎙️ Voice AI Capabilities**
- **Natural Language Processing** - Understands complex coffee orders
- **Real-time Speech Recognition** - Powered by AssemblyAI
- **High-Quality Text-to-Speech** - Natural voice responses
- **Multi-turn Conversations** - Handles incomplete orders intelligently

### **🤖 Autonomous Agent Behavior**
- **Independent Decision-Making** - Validates order completeness automatically
- **Adaptive Responses** - Asks clarifying questions when needed
- **State Management** - Tracks order progress autonomously
- **Error Handling** - Gracefully handles missing information

### **📊 Real-Time Visualization**
- **Dynamic Order Display** - Visual cup builder updates as you speak
- **Animated Receipts** - Professional order confirmations
- **Live Status Updates** - Real-time order progress tracking
- **Modern Dark UI** - Sleek coffee shop themed interface

## 🛠️ **Tech Stack**

### **Backend (Python)**
- **LiveKit Agents** - Real-time voice processing framework
- **Google Gemini** - Large Language Model for conversation
- **AssemblyAI** - Speech-to-Text recognition
- **AI Voice Technology** - Text-to-Speech synthesis
- **Python 3.9+** - Core backend language

### **Frontend (Next.js)**
- **Next.js 15** - React framework with App Router
- **React 19** - Modern UI components
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **LiveKit Client SDK** - Real-time communication

## 📋 **Project Structure**

```
AgentX-Coffee-Shop/
├── backend/                 # Python voice agent
│   ├── src/
│   │   └── agent.py        # Main agent logic
│   ├── orders/             # Saved order files
│   ├── run.bat            # Windows startup script
│   ├── pyproject.toml     # Python dependencies
│   └── README.md          # Backend documentation
├── frontend/               # Next.js web interface
│   ├── app/               # Next.js app directory
│   ├── components/        # React components
│   ├── app-config.ts      # App configuration
│   └── README.md          # Frontend documentation
├── start-all.bat          # Complete system startup
└── README.md              # This file
```

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- API Keys: Google AI, AssemblyAI

### **1. Clone & Setup**
```bash
git clone <repository-url>
cd AgentX-Coffee-Shop
```

### **2. Backend Setup**
```bash
cd backend
uv sync
cp .env.example .env.local
# Edit .env.local with your API keys
```

### **3. Frontend Setup**
```bash
cd frontend
pnpm install
cp .env.example .env.local
# Edit .env.local with LiveKit credentials
```

### **4. Run the Application**
```bash
# Option 1: Run all services
.\start-all.bat

# Option 2: Run individually
# Terminal 1: Backend
cd backend && .\run.bat

# Terminal 2: Frontend
cd frontend && pnpm dev
```

### **5. Access the Application**
Open **http://localhost:3000** in your browser and start ordering coffee with your voice!

## 🎯 **How It Works**

### **1. Voice Interaction Flow**
1. **User speaks** their coffee order
2. **Speech Recognition** converts voice to text
3. **AI Agent** processes the request using Gemini
4. **Order Validation** checks for completeness
5. **Visual Feedback** updates the UI in real-time
6. **Voice Response** confirms or asks for clarification
7. **Order Completion** generates receipt and saves data

### **2. Autonomous Decision-Making**
- **Order Validation** - Automatically checks for required information
- **Conversation Management** - Decides when to ask follow-up questions
- **State Tracking** - Maintains order context across interactions
- **Error Recovery** - Handles misunderstandings gracefully

## 🏆 **Competition Highlights**

### **Innovation & Originality**
- **First-of-its-kind** voice coffee ordering system
- **Real-time visual feedback** during voice interactions
- **Autonomous order management** with intelligent validation

### **Technical Excellence**
- **Production-ready architecture** with proper error handling
- **Scalable design** supporting multiple concurrent users
- **Real-time performance** with low-latency voice processing

### **Practical Impact**
- **Immediate business value** for coffee shops and restaurants
- **Enhanced customer experience** with voice-first interface
- **Accessibility benefits** for users with mobility limitations

## 👥 **Team Information**

**Team Size:** 5 Members  
**Competition:** AgentX - Agentic Development Competition  
**University:** Woxsen University, Hyderabad  
**Date:** February 4, 2026  

## 📊 **Demo Instructions**

### **For Judges/Evaluators:**
1. **Start the application** using the Quick Start guide
2. **Open http://localhost:3000** in your browser
3. **Click "Start Ordering"** to begin voice interaction
4. **Speak your coffee order** (e.g., "I'd like a large latte with oat milk")
5. **Watch real-time visualization** as the order builds
6. **Complete the order** by providing your name
7. **View the generated receipt** and saved order data

### **Sample Orders to Try:**
- *"Hi, I'd like a medium cappuccino with almond milk and extra foam"*
- *"Can I get a large americano with no milk and an extra shot?"*
- *"I want a small mocha with whipped cream, my name is Alex"*

## 🔧 **API Keys Required**

```bash
# Backend (.env.local)
GOOGLE_API_KEY=your_google_api_key
MURF_API_KEY=your_murf_api_key  
ASSEMBLYAI_API_KEY=your_assemblyai_key
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_livekit_key
LIVEKIT_API_SECRET=your_livekit_secret
```

## 🎯 **Future Enhancements**

- **Multi-language Support** - Hindi, Telugu voice ordering
- **Customer Analytics** - Order trends and insights dashboard
- **Loyalty Program** - Points and rewards system
- **Mobile App** - Native iOS/Android applications
- **Payment Integration** - Complete order-to-payment flow

## 📄 **License**

MIT License - Built for AgentX Competition 2026

## 🙏 **Acknowledgments**

- **LiveKit** - Real-time communication platform
- **Google AI** - Gemini language model
- **AssemblyAI** - Speech recognition technology
- **Woxsen University** - Hosting the AgentX Competition
- **Our Team** - 5 dedicated developers building the future of voice AI

---

⭐ **Star this repo if you find it helpful!**

**Built with ❤️ for AgentX - Agentic Development Competition 2026**

---

## 👥 **Team Collaboration**

This project represents the collaborative effort of our 5-member development team for the **AgentX - Agentic Development Competition 2026** at Woxsen University. Each team member contributed their expertise in AI development, frontend engineering, system architecture, and user experience design to create this autonomous voice assistant.

**🎓 Developed at Woxsen University, Hyderabad**