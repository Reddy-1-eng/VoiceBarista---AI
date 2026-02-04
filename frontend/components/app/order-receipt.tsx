'use client';

import React, { useState } from 'react';
import { useDataChannel } from '@livekit/components-react';
import { motion, AnimatePresence } from 'motion/react';

export function OrderReceipt() {
  const [receiptHtml, setReceiptHtml] = useState<string>('');
  const [isVisible, setIsVisible] = useState(false);

  // Listen for receipt data from the agent
  useDataChannel('order_receipt', (message) => {
    const decoder = new TextDecoder();
    const html = decoder.decode(message.payload);
    setReceiptHtml(html);
    setIsVisible(true);
    
    // Auto-hide after 15 seconds
    setTimeout(() => {
      setIsVisible(false);
    }, 15000);
  });

  if (!isVisible || !receiptHtml) {
    return null;
  }

  return (
    <AnimatePresence mode="wait">
      {isVisible && (
        <>
          {/* Backdrop */}
          <motion.div
            key="receipt-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-[59]"
            onClick={() => setIsVisible(false)}
          />
          
          {/* Receipt */}
          <motion.div
            key="receipt-content"
            initial={{ opacity: 0, scale: 0.8, y: 50 }}
            animate={{ 
              opacity: 1, 
              scale: 1, 
              y: 0,
              transition: {
                duration: 0.6,
                ease: [0.34, 1.56, 0.64, 1],
              }
            }}
            exit={{ 
              opacity: 0, 
              scale: 0.8,
              y: 50,
              transition: { duration: 0.4 }
            }}
            className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-[60] max-w-md"
            style={{ pointerEvents: 'none' }}
          >
            <div
              dangerouslySetInnerHTML={{ __html: receiptHtml }}
              style={{ pointerEvents: 'auto' }}
            />
            
            {/* Close button */}
            <button
              onClick={() => setIsVisible(false)}
              className="absolute top-2 right-2 bg-amber-600 hover:bg-amber-700 text-white rounded-full w-8 h-8 flex items-center justify-center text-lg font-bold shadow-lg transition-colors"
              style={{ pointerEvents: 'auto' }}
            >
              ×
            </button>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
