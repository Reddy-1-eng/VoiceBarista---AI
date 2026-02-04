'use client';

import React, { useEffect, useState } from 'react';
import { useDataChannel } from '@livekit/components-react';
import { motion, AnimatePresence } from 'motion/react';

export function DrinkVisualization() {
  const [drinkHtml, setDrinkHtml] = useState<string>('');
  const [isVisible, setIsVisible] = useState(false);
  const [key, setKey] = useState(0);

  // Listen for drink visualization data from the agent
  useDataChannel('drink_visualization', (message) => {
    const decoder = new TextDecoder();
    const html = decoder.decode(message.payload);
    setDrinkHtml(html);
    setIsVisible(true);
    setKey(prev => prev + 1); // Force re-render with new animation
  });

  if (!isVisible || !drinkHtml) {
    return null;
  }

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={key}
        initial={{ opacity: 0, scale: 0.9, x: 20 }}
        animate={{ 
          opacity: 1, 
          scale: 1, 
          x: 0,
          transition: {
            duration: 0.5,
            ease: [0.34, 1.56, 0.64, 1], // Smooth bounce
          }
        }}
        exit={{ 
          opacity: 0, 
          scale: 0.95, 
          transition: { duration: 0.2 }
        }}
        className="fixed top-1/2 right-6 -translate-y-1/2 z-50 max-w-md"
        style={{ pointerEvents: 'none' }}
      >
        <div
          dangerouslySetInnerHTML={{ __html: drinkHtml }}
          style={{ pointerEvents: 'auto' }}
        />
      </motion.div>
    </AnimatePresence>
  );
}
