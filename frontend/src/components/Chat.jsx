import React, { useState, useEffect, useRef } from 'react';
import { useAppContext } from '../context/AppContext';
import { Mic, MicOff, Send } from 'lucide-react';

export default function Chat() {
  const { t } = useAppContext();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  
  const recognitionRef = useRef(null);

  useEffect(() => {
    // Initialize first message based on current language
    if (messages.length === 0) {
      setMessages([{ role: 'assistant', text: t.chat_welcome }]);
    } else {
      // Update first message if language changes
      setMessages(prev => {
        const newMsgs = [...prev];
        if (newMsgs[0].role === 'assistant') {
          newMsgs[0].text = t.chat_welcome;
        }
        return newMsgs;
      });
    }

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.lang = 'es-ES'; // Default, ideally from context
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(prev => prev + " " + transcript);
        setIsListening(false);
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error("Speech recognition error", event.error);
        setIsListening(false);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }
  }, [t]); // Depend on translation to update welcome msg

  const toggleListen = () => {
    if (isListening) {
      recognitionRef.current?.stop();
      setIsListening(false);
    } else {
      recognitionRef.current?.start();
      setIsListening(true);
    }
  };

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMsg = input.trim();
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setInput('');
    setIsTyping(true);

    setTimeout(() => {
      let botResponse = "Interesante pregunta. Este sistema utiliza redes neuronales convolucionales híbridas para analizar patrones en la hoja.";
      if (userMsg.toLowerCase().includes("bacterial")) {
        botResponse = "La mancha bacteriana es causada por Xanthomonas campestris. Se recomienda usar bactericidas a base de cobre y rotar cultivos.";
      } else if (userMsg.toLowerCase().includes("hola") || userMsg.toLowerCase().includes("hello")) {
        botResponse = t.chat_welcome;
      }

      setMessages(prev => [...prev, { role: 'assistant', text: botResponse }]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 flex flex-col h-[600px] overflow-hidden">
      <div className="p-4 bg-gray-900 border-b border-gray-700">
        <h3 className="font-bold text-emerald-400 flex items-center">
          <span className="text-xl mr-2">🤖</span> {t.chat_title}
        </h3>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-lg ${msg.role === 'user' ? 'bg-emerald-600 text-white rounded-br-none' : 'bg-gray-700 text-gray-200 rounded-bl-none'}`}>
              {msg.text}
            </div>
          </div>
        ))}
        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-gray-700 text-gray-400 p-3 rounded-lg rounded-bl-none italic text-sm">
              {t.processing}...
            </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-gray-900 border-t border-gray-700">
        <form onSubmit={handleSend} className="flex space-x-2">
          <button
            type="button"
            onClick={toggleListen}
            className={`p-3 rounded-lg flex items-center justify-center transition-colors ${isListening ? 'bg-red-500 text-white animate-pulse' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}
            title="Hablar por micrófono"
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t.chat_input}
            className="flex-1 bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-emerald-500"
          />
          <button 
            type="submit" 
            disabled={!input.trim() || isTyping}
            className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-700 disabled:text-gray-500 text-white px-6 py-2 rounded-lg font-bold transition-colors flex items-center"
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  );
}
