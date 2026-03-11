'use client';

import { useState, useEffect, useRef } from 'react';
import { useRouter } from 'next/navigation';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
};

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Authentication check
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    } else {
      // Add initial greeting
      setMessages([
        {
          id: 'initial',
          role: 'assistant',
          content: 'Hello! I am your Smart Campus Assistant. How can I help you today?'
        }
      ]);
    }
  }, [router]);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_role');
    router.push('/login');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userQuery = input.trim();
    setInput('');

    // Add user message to UI immediately
    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: userQuery };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const res = await fetch(`${backendUrl}/chat/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ query: userQuery }),
      });

      if (res.status === 401) {
        handleLogout();
        return;
      }

      if (!res.ok) throw new Error('Failed to fetch response');
      console.log("1");
      const data = await res.json();
      console.log("2");
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.response || 'I processed your request.'
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, {
        id: Date.now().toString(),
        role: 'assistant',
        content: "I'm sorry, I'm having trouble connecting to the campus systems right now. Please try again later."
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-[#09090b]">
      {/* Header */}
      <header className="flex-none bg-zinc-900/80 backdrop-blur-md border-b border-zinc-800 p-4 sticky top-0 z-10 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <span className="text-white font-bold text-sm">SC</span>
          </div>
          <div>
            <h1 className="text-lg font-semibold text-white tracking-tight">Afeka Assistant</h1>
            <p className="text-xs text-green-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-green-400"></span> Online
            </p>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="text-sm text-zinc-400 hover:text-white transition-colors px-3 py-1.5 rounded-lg hover:bg-zinc-800"
        >
          Sign out
        </button>
      </header>

      {/* Chat History Area */}
      <main className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-6">
        <div className="max-w-3xl mx-auto w-full space-y-6">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'} w-full`}
            >
              <div
                className={`max-w-[85%] sm:max-w-[75%] rounded-2xl px-5 py-3.5 shadow-sm transform transition-all ${msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-sm'
                    : 'bg-zinc-800 text-zinc-100 rounded-tl-sm border border-zinc-700/50'
                  }`}
              >
                <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>
              </div>
            </div>
          ))}

          {/* Typing Indicator */}
          {isLoading && (
            <div className="flex justify-start w-full animate-in fade-in slide-in-from-bottom-2">
              <div className="bg-zinc-800 border border-zinc-700/50 rounded-2xl rounded-tl-sm px-5 py-4 w-16">
                <div className="flex space-x-1.5">
                  <div className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
                  <div className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
                  <div className="w-1.5 h-1.5 bg-zinc-400 rounded-full animate-bounce"></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input Form Area */}
      <div className="flex-none bg-zinc-900 border-t border-zinc-800 p-4 pb-6 sm:p-6">
        <div className="max-w-3xl mx-auto w-full">
          <form
            onSubmit={handleSubmit}
            className="relative flex items-end bg-zinc-950/50 border border-zinc-700/80 rounded-2xl focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all shadow-xl"
          >
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSubmit(e);
                }
              }}
              placeholder="Ask about courses, exams, lecturers..."
              className="w-full max-h-32 min-h-[56px] bg-transparent text-white px-5 py-4 focus:outline-none resize-none placeholder:text-zinc-500 disabled:opacity-50"
              rows={1}
              disabled={isLoading}
            />
            <div className="p-2 sm:p-3">
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="bg-blue-600 hover:bg-blue-500 text-white p-2.5 rounded-xl transition-colors disabled:opacity-50 disabled:bg-zinc-800 disabled:text-zinc-500 transform active:scale-95"
              >
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
                  <path d="M3.478 2.404a.75.75 0 00-.926.941l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.404z" />
                </svg>
              </button>
            </div>
          </form>
          <p className="text-center text-xs text-zinc-500 mt-3 hidden sm:block">
            Smart Campus Assistant uses AI. Check important information manually.
          </p>
        </div>
      </div>
    </div>
  );
}
