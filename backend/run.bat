@echo off
REM Copy this file to run.bat and add your API keys
set LIVEKIT_URL=wss://agentic-0odrgqux.livekit.cloud
set LIVEKIT_API_KEY=APIxEvWPucaamvf
set LIVEKIT_API_SECRET=7qKYc6PAqtIpnGKmvbNvuWgtjoyTs0ouKCY58dteX9C
set GOOGLE_API_KEY=your_google_api_key_here
set GROQ_API_KEY=your_groq_api_key_here
set MURF_API_KEY=your_murf_api_key_here
set ASSEMBLYAI_API_KEY=your_assemblyai_api_key_here
set DEEPGRAM_API_KEY=
uv run python src/agent.py dev
