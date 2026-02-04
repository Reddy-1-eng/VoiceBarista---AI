import { Button } from '@/components/livekit/button';

function CoffeeIcon() {
  return (
    <div className="relative mb-12">
      <div className="text-8xl animate-bounce">☕</div>
      <div className="absolute -top-2 -right-2 text-4xl animate-pulse">✨</div>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref} className="min-h-screen bg-gradient-to-br from-gray-800 via-gray-900 to-slate-900 relative overflow-hidden">
      {/* Floating Background Icons - Restored */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Floating food icons with better visibility */}
        <div className="absolute top-20 left-10 text-5xl opacity-20 animate-float text-amber-400">☕</div>
        <div className="absolute top-40 right-20 text-4xl opacity-20 animate-float-delayed text-orange-400">🥐</div>
        <div className="absolute bottom-32 left-1/4 text-6xl opacity-20 animate-float text-pink-400">🍰</div>
        <div className="absolute bottom-20 right-1/3 text-5xl opacity-20 animate-float-delayed text-purple-400">🧁</div>
        
        {/* Minimal geometric shapes */}
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-blue-500/10 rounded-full blur-2xl"></div>
        <div className="absolute bottom-1/4 right-1/4 w-72 h-72 bg-purple-500/10 rounded-full blur-2xl"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-full blur-3xl"></div>
      </div>

      <section className="relative z-10 flex flex-col items-center justify-center text-center min-h-screen px-4 py-8">
        {/* Logo/Icon */}
        <CoffeeIcon />

        {/* Clean, minimal title */}
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-light text-white mb-8 tracking-tight">
          AgentX Coffee Shop
        </h1>

        {/* Minimal subtitle */}
        <p className="text-xl md:text-2xl text-gray-300 mb-6 max-w-3xl leading-relaxed font-normal">
          Your AI Barista is Ready to Take Your Order
        </p>

        {/* Clean description */}
        <p className="text-base md:text-lg text-gray-400 mb-12 max-w-2xl leading-relaxed">
          Experience the future of coffee ordering with our intelligent voice assistant
        </p>

        {/* Minimal, clean button */}
        <div className="relative group mb-16">
          <Button 
            variant="primary" 
            size="lg" 
            onClick={onStartCall} 
            className="px-12 md:px-16 py-4 md:py-6 text-lg md:text-xl font-medium bg-white text-gray-800 hover:bg-gray-100 transition-all duration-300 shadow-lg hover:shadow-xl rounded-full border border-gray-200"
          >
            🎤 {startButtonText}
          </Button>
        </div>

        {/* Minimal feature highlights */}
        <div className="flex flex-wrap justify-center gap-6 md:gap-8 max-w-4xl">
          <div className="flex items-center space-x-3 text-gray-300 hover:text-white transition-colors duration-300 px-4 py-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <span className="text-xl md:text-2xl">🎙️</span>
            <span className="text-sm md:text-base font-medium">Voice Powered</span>
          </div>
          <div className="flex items-center space-x-3 text-gray-300 hover:text-white transition-colors duration-300 px-4 py-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <span className="text-xl md:text-2xl">⚡</span>
            <span className="text-sm md:text-base font-medium">Lightning Fast</span>
          </div>
          <div className="flex items-center space-x-3 text-gray-300 hover:text-white transition-colors duration-300 px-4 py-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <span className="text-xl md:text-2xl">🤖</span>
            <span className="text-sm md:text-base font-medium">AI Powered</span>
          </div>
          <div className="flex items-center space-x-3 text-gray-300 hover:text-white transition-colors duration-300 px-4 py-2 rounded-full bg-gray-800/50 backdrop-blur-sm border border-gray-700/50">
            <span className="text-xl md:text-2xl">☕</span>
            <span className="text-sm md:text-base font-medium">Perfect Orders</span>
          </div>
        </div>
      </section>

      {/* Minimal footer */}
      <div className="absolute bottom-8 left-0 right-0 flex justify-center z-20">
        <div className="bg-gray-800/70 backdrop-blur-sm rounded-full px-6 py-3 border border-gray-700/50">
          <p className="text-gray-400 text-sm font-medium">
            Built with ❤️ for AgentX Competition 2026
          </p>
        </div>
      </div>

      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-15px); }
        }
        @keyframes float-delayed {
          0%, 100% { transform: translateY(0px); }
          50% { transform: translateY(-12px); }
        }
        .animate-float {
          animation: float 8s ease-in-out infinite;
        }
        .animate-float-delayed {
          animation: float-delayed 10s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};
