import { Send } from 'lucide-react';
import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { formatResponse } from '@/lib/strings';

interface ChatPaneProps {
  activeTools: string[];
}

export function ChatPane({ activeTools }: ChatPaneProps) {
  const [messages, setMessages] = useState<
    Array<{ role: 'user' | 'assistant'; content: string }>
  >([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message to chat
    const userMessage = { role: 'user' as const, content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Call API with selected tools and user message
      const response = await fetch('http://localhost:8001/powerup-demo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          tools: activeTools,
          message: input,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      // Add assistant response to chat
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error('Error calling PowerUp API:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, there was an error processing your request.',
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='flex h-full w-1/2 flex-col rounded-[1.5rem]'>
      <div className='flex-1 space-y-4 overflow-y-auto p-6'>
        {messages.map((message, i) => (
          <motion.div
            key={i}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div
              className={`max-w-[80%] rounded-lg p-3`}
              style={{
                background:
                  message.role === 'user'
                    ? 'linear-gradient(90deg, rgba(0, 135, 145, 0.7) 0%, rgba(129, 255, 254, 0.3) 100%)'
                    : 'rgba(0, 40, 43, 0.7)',
                backdropFilter: 'blur(8px)',
                color: 'rgba(255, 255, 255, 0.9)',
              }}
            >
              {formatResponse(message.content)}
            </div>
          </motion.div>
        ))}
        {isLoading && (
          <motion.div
            className='flex justify-start'
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <div
              className='max-w-[80%] rounded-lg p-3'
              style={{
                background: 'rgba(0, 40, 43, 0.7)',
                backdropFilter: 'blur(8px)',
                color: 'rgba(255, 255, 255, 0.9)',
              }}
            >
              <div className='flex space-x-2'>
                <div className='h-2 w-2 animate-pulse rounded-full bg-[#81FFFE]'></div>
                <div
                  className='h-2 w-2 animate-pulse rounded-full bg-[#81FFFE]'
                  style={{ animationDelay: '0.2s' }}
                ></div>
                <div
                  className='h-2 w-2 animate-pulse rounded-full bg-[#81FFFE]'
                  style={{ animationDelay: '0.4s' }}
                ></div>
              </div>
            </div>
          </motion.div>
        )}
      </div>
      <form
        onSubmit={handleSubmit}
        className='border-t border-[rgba(255,255,255,0.1)] p-4'
      >
        <div className='flex gap-2'>
          <input
            type='text'
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className='joyful-input flex-1 rounded-lg border border-[rgba(255,255,255,0.1)] p-2'
            placeholder='Type your message...'
          />
          <button
            type='submit'
            className='rounded-lg p-2 text-white'
            style={{
              background:
                'linear-gradient(90deg, rgba(0, 135, 145, 0.9) 0%, rgba(129, 255, 254, 0.6) 100%)',
              boxShadow: '0px 0px 10px rgba(129, 255, 254, 0.3)',
            }}
          >
            <Send className='h-5 w-5' />
          </button>
        </div>
      </form>
    </div>
  );
}
