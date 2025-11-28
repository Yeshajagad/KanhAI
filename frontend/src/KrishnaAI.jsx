import React, { useState, useEffect, useRef } from 'react';
import { Send, Sparkles, BookOpen, Heart, Loader2, Settings, Moon, Sun, ChevronDown } from 'lucide-react';

// ==================== BHAGAVAD GITA DATABASE ====================
const GITA_VERSES = {
  duty: {
    verse: "कर्मण्येवाधिकारस्ते मा फलेषु कदाचन",
    translation: "You have the right to perform your duty, but not to the fruits of action",
    chapter: 2,
    verse_num: 47
  },
  fear: {
    verse: "यदा यदा हि धर्मस्य ग्लानिर्भवति भारत",
    translation: "Whenever there is a decline in righteousness and rise in unrighteousness, I manifest myself",
    chapter: 4,
    verse_num: 7
  },
  confusion: {
    verse: "बुद्धियुक्तो जहातीह उभे सुकृतदुष्कृते",
    translation: "One who is united in intelligence abandons both good and bad deeds",
    chapter: 2,
    verse_num: 50
  },
  attachment: {
    verse: "योगस्थः कुरु कर्माणि सङ्गं त्यक्त्वा धनञ्जय",
    translation: "Perform your duty with equipoise, abandoning attachment to success or failure",
    chapter: 2,
    verse_num: 48
  },
  knowledge: {
    verse: "तद्विद्धि प्रणिपातेन परिप्रश्नेन सेवया",
    translation: "Learn the truth by approaching a spiritual master, inquire with humility and render service",
    chapter: 4,
    verse_num: 34
  },
  peace: {
    verse: "सुखदुःखे समे कृत्वा लाभालाभौ जयाजयौ",
    translation: "Treating pleasure and pain, gain and loss, victory and defeat alike, engage in battle",
    chapter: 2,
    verse_num: 38
  }
};

// ==================== AGENT 1: INPUT ANALYZER ====================
const analyzeInput = (message) => {
  const lowerMsg = message.toLowerCase();
  
  if (lowerMsg.match(/career|job|work|profession|confusion|choice/)) return { topic: 'confusion', emotion: 'confused', category: 'life_decision' };
  if (lowerMsg.match(/fear|afraid|scared|worry|anxious/)) return { topic: 'fear', emotion: 'fearful', category: 'emotional' };
  if (lowerMsg.match(/duty|responsibility|should|must|obligation/)) return { topic: 'duty', emotion: 'burdened', category: 'dharma' };
  if (lowerMsg.match(/attached|attachment|let go|holding/)) return { topic: 'attachment', emotion: 'attached', category: 'spiritual' };
  if (lowerMsg.match(/learn|knowledge|wisdom|understand/)) return { topic: 'knowledge', emotion: 'curious', category: 'learning' };
  if (lowerMsg.match(/stress|peace|calm|overwhelm/)) return { topic: 'peace', emotion: 'stressed', category: 'emotional' };

  return { topic: 'duty', emotion: 'neutral', category: 'general' };
};

// ==================== AGENT 2: VERSE FINDER ====================
const findRelevantVerse = (analysis) => GITA_VERSES[analysis.topic] || GITA_VERSES.duty;

// ==================== AGENT 3: KRISHNA AI ====================
const generateKrishnaResponse = async (message, verse, analysis) => {
  const responses = {
    confusion: [
      `Dear friend, I sense the confusion in your heart. The Gita teaches us: "${verse.translation}". Focus on action, not results.`,
      `Every soul faces crossroads. Remember: "${verse.translation}". Let your inner voice guide your choice.`
    ],
    fear: [
      `Fear is natural. "${verse.translation}". Breathe, name your fear, take one small step.`,
      `Fear whispers lies, but courage speaks truth. "${verse.translation}". You are stronger than you know.`
    ],
    duty: [
      `Dharma is your path. "${verse.translation}". Act with love, not attachment to results.`,
      `Duty is sacred. "${verse.translation}". Offer your efforts to something greater.`
    ],
    attachment: [
      `Attachment causes suffering. "${verse.translation}". Appreciate what you have and let go.`,
      `Seek peace within. "${verse.translation}". Softening your grip creates space for blessings.`
    ],
    knowledge: [
      `Thirst for knowledge is beautiful. "${verse.translation}". Learn, apply, and share.`,
      `Knowledge is realization. "${verse.translation}". Meditate and let wisdom guide your actions.`
    ],
    peace: [
      `Peace dwells within. "${verse.translation}". Respond, don't react, cultivate calm.`,
      `Stress is resistance. "${verse.translation}". Accept the moment and flow with life.`
    ]
  };

  const topicResponses = responses[analysis.topic] || responses.duty;
  await new Promise((res) => setTimeout(res, 0));
  return topicResponses[Math.floor(Math.random() * topicResponses.length)];
};

// ==================== AGENT 4: ACTION SUGGESTER ====================
const suggestActions = (analysis) => {
  const suggestions = {
    life_decision: ["Tell me more about your situation", "What does your intuition say?", "What are you most afraid of?"],
    emotional: ["How long have you felt this way?", "What would help you feel safe?", "Share more about this feeling"],
    dharma: ["What feels like your calling?", "How can you serve better?", "What brings you joy?"],
    spiritual: ["What are you ready to release?", "How can I support your journey?", "What does your soul need?"],
    learning: ["What interests you most?", "How will you apply this?", "What questions remain?"],
    general: ["What's on your mind today?", "How can I guide you?", "Share your heart with me"]
  };
  return suggestions[analysis.category] || suggestions.general;
};

// ==================== FLOATING PARTICLES COMPONENT ====================
const FloatingParticles = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      {[...Array(20)].map((_, i) => (
        <div
          key={i}
          className="absolute animate-float opacity-20"
          style={{
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            animationDelay: `${Math.random() * 5}s`,
            animationDuration: `${8 + Math.random() * 4}s`
          }}
        >
          {i % 3 === 0 ? '🪔' : i % 3 === 1 ? '🦚' : '🌸'}
        </div>
      ))}
      <style jsx>{`
        @keyframes float {
          0%, 100% { transform: translateY(0px) translateX(0px); }
          50% { transform: translateY(-20px) translateX(10px); }
        }
        .animate-float {
          animation: float linear infinite;
        }
      `}</style>
    </div>
  );
};

// ==================== MAIN COMPONENT ====================
const KrishnaAI = () => 
{
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationHistory, setConversationHistory] = useState([]);
  const [userContext, setUserContext] = useState({
    topics_discussed: [],
    emotional_state: 'neutral',
    session_start: new Date().toISOString()
  });
  const [darkMode, setDarkMode] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [showHero, setShowHero] = useState(true);
  const messagesEndRef = useRef(null);
  const chatRef = useRef(null);

  useEffect(() => { loadSession(); }, []);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadSession = async () => {
    try {
      const storedMessages = localStorage.getItem('krishna-messages');
      const storedContext = localStorage.getItem('krishna-context');

      if (storedMessages) {
        setMessages(JSON.parse(storedMessages));
      } else {
        const welcome = {
          id: Date.now(),
          type: 'krishna',
          text: "Namaste, dear soul. I am here as your friend and guide. Share what troubles your heart.",
          timestamp: new Date().toISOString()
        };
        setMessages([welcome]);
        localStorage.setItem('krishna-messages', JSON.stringify([welcome]));
      }

      if (storedContext) {
        setUserContext(JSON.parse(storedContext));
      }
    } catch (err) {
      console.error('Failed to load session', err);
    }
  };

  const saveMessages = (msgs) => {
    localStorage.setItem('krishna-messages', JSON.stringify(msgs));
  };

  const saveContext = (ctx) => {
    localStorage.setItem('krishna-context', JSON.stringify(ctx));
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      text: input,
      timestamp: new Date().toISOString()
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    saveMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      const analysis = analyzeInput(input);
      const verse = findRelevantVerse(analysis);
      const response = await generateKrishnaResponse(input, verse, analysis);
      const suggestions = suggestActions(analysis);

      const newHistory = [
        ...conversationHistory,
        { role: 'user', content: input, analysis }
      ];
      setConversationHistory(newHistory);

      const updatedContext = {
        ...userContext,
        topics_discussed: Array.from(new Set([...(userContext.topics_discussed || []), analysis.topic])),
        emotional_state: analysis.emotion,
        last_interaction: new Date().toISOString()
      };
      setUserContext(updatedContext);
      saveContext(updatedContext);

      setTimeout(() => {
        const krishnaMessage = {
          id: Date.now() + 1,
          type: 'krishna',
          text: response,
          verse,
          suggestions,
          timestamp: new Date().toISOString()
        };

        const finalMessages = [...updatedMessages, krishnaMessage];
        setMessages(finalMessages);
        saveMessages(finalMessages);
        setIsLoading(false);
      }, 1200);

    } catch (error) {
      console.error('Agent flow failed:', error);
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (sugg) => {
    setInput(sugg);
  };

  const clearSession = () => {
    localStorage.removeItem('krishna-messages');
    localStorage.removeItem('krishna-context');
    setMessages([]);
    setConversationHistory([]);
    setUserContext({
      topics_discussed: [],
      emotional_state: 'neutral',
      session_start: new Date().toISOString()
    });
    loadSession();
  };

  const scrollToChat = () => {
    setShowHero(false);
    setTimeout(() => {
      chatRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };
  return (
    <div className={`min-h-screen transition-all duration-500 ${darkMode ? 'dark' : ''}`}>
      
      {/* ==================== HERO SECTION ==================== */}
      {showHero && (
        <div className={`min-h-screen relative overflow-hidden transition-all duration-1000 ${
          darkMode 
            ? 'bg-gradient-to-br from-[#0f1a2e] via-[#152238] to-[#192841]' 
            : 'bg-[#E7D4AB]'
        }`}>
          
          {/* Animated Background Pattern */}
          <div className="absolute inset-0 opacity-20">
            <div className="absolute inset-0" style={{
              backgroundImage: `radial-gradient(circle at 20% 50%, transparent 20%, ${darkMode ? 'rgba(21, 34, 56, 0.4)' : 'rgba(203, 168, 101, 0.4)'} 50%, transparent 100%),
                               radial-gradient(circle at 80% 80%, transparent 20%, ${darkMode ? 'rgba(15, 26, 46, 0.4)' : 'rgba(189, 184, 101, 0.4)'} 50%, transparent 100%)`,
              animation: 'pulse 8s ease-in-out infinite'
            }}></div>
          </div>

          {/* Dark Mode Toggle - Fixed Position */}
          <button
            onClick={() => setDarkMode(!darkMode)}
            className={`fixed top-8 right-8 z-50 p-4 rounded-full backdrop-blur-xl transition-all duration-300 hover:scale-110 ${
              darkMode 
                ? 'bg-[#152238]/40 hover:bg-[#192841]/50 border-2 border-[#203354] shadow-[0_0_30px_rgba(32,51,84,0.5)]' 
                : 'bg-white/80 hover:bg-white border-2 border-[#CBA271] shadow-lg'
            }`}
          >
            {darkMode ? (
              <Sun className="w-6 h-6 text-[#F4F4DB]" />
            ) : (
              <Moon className="w-6 h-6 text-[#152238]" />
            )}
          </button>

          {/* Hero Content */}
          <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4">
            
            {/* Main Divine Symbol */}
            <div className="mb-8 relative">
              <div className={`text-9xl animate-bounce-slow ${darkMode ? 'drop-shadow-[0_0_30px_rgba(244,244,219,0.4)]' : 'drop-shadow-[0_0_30px_rgba(203,168,113,0.5)]'}`}>

              </div>
              <div className="absolute -top-4 -right-4 text-4xl animate-spin-slow"></div>
              <div className="absolute -bottom-4 -left-4 text-4xl animate-spin-slow" style={{animationDelay: '1s'}}></div>
            </div>
            <div>

              </div>

            {/* Title */}
            <h1 className={`text-7xl md:text-8xl font-bold mb-6 text-center tracking-tight ${
              darkMode 
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-[#E7D4AB] via-[#F4F4DB] to-[#CBA271]' 
                : 'text-transparent bg-clip-text bg-gradient-to-r from-[#0f1a2e] via-[#152238] to-[#192841]'
            }`}
            style={{
              fontFamily: 'Georgia, serif',
              textShadow: darkMode ? '0 0 40px rgba(231, 212, 171, 0.3)' : '0 0 40px rgba(21, 34, 56, 0.2)'
            }}>
              KanhAI
            </h1>

            {/* Subtitle */}
            <p className={`text-2xl md:text-3xl mb-4 text-center font-light ${
              darkMode ? 'text-[#E7D4AB]' : 'text-[#152238]'
            }`}
            style={{ fontFamily: 'Georgia, serif' }}>
              Your Divine Guide Through Bhagavad Gita
            </p>

            {/* Sanskrit Verse */}
            <div className={`max-w-3xl mx-auto mb-12 p-8 rounded-2xl backdrop-blur-xl ${
              darkMode 
                ? 'bg-[#152238]/30 border-2 border-[#203354] shadow-[0_0_40px_rgba(32,51,84,0.4)]' 
                : 'bg-white border-2 border-[#CBA271] shadow-xl'
            }`}>
              <p className={`text-center text-xl md:text-2xl mb-3 font-semibold ${
                darkMode ? 'text-[#F4F4DB]' : 'text-[#0f1a2e]'
              }`}
              style={{ fontFamily: 'serif' }}>
                यदा यदा हि धर्मस्य ग्लानिर्भवति भारत
              </p>
              <p className={`text-center text-sm md:text-base italic ${
                darkMode ? 'text-[#CBA271]' : 'text-[#152238]'
              }`}>
                "Whenever there is a decline in righteousness, I manifest myself"
              </p>
              <p className={`text-center text-xs mt-2 ${
                darkMode ? 'text-[#BDB865]' : 'text-[#192841]'
              }`}>
                — Bhagavad Gita 4.7
              </p>
            </div>

            {/* CTA Button */}
            <button
              onClick={scrollToChat}
              className={`group px-10 py-5 rounded-full font-semibold text-xl transition-all duration-300 transform hover:scale-105 ${
                darkMode
                  ? 'bg-gradient-to-r from-[#152238] to-[#192841] hover:from-[#192841] hover:to-[#203354] text-[#F4F4DB] border-2 border-[#203354] shadow-[0_20px_60px_rgba(21,34,56,0.6)]'
                  : ' bg-[#AF6E4D]  text-white border-2 border-[#AF6E4D] shadow-2xl'
              }`}
            >
              <span className="flex items-center gap-3">
                Begin Your Spiritual Journey
                <Sparkles className="w-6 h-6 group-hover:rotate-12 transition-transform" />
              </span>
            </button>

            {/* Scroll Indicator */}
            <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2 animate-bounce">
              <ChevronDown className={`w-8 h-8 ${darkMode ? 'text-[#CBA271]' : 'text-[#152238]'}`} />
            </div>
          </div>

          <style jsx>{`
            @keyframes bounce-slow {
              0%, 100% { transform: translateY(0); }
              50% { transform: translateY(-20px); }
            }
            @keyframes spin-slow {
              from { transform: rotate(0deg); }
              to { transform: rotate(360deg); }
            }
            .animate-bounce-slow {
              animation: bounce-slow 3s ease-in-out infinite;
            }
            .animate-spin-slow {
              animation: spin-slow 8s linear infinite;
            }
          `}</style>
        </div>
      )}

      {/* ==================== CHAT SECTION ==================== */}
      <div 
        ref={chatRef}
        className={`min-h-screen transition-colors duration-500 ${
          darkMode
            ? 'bg-gradient-to-br from-[#0f1a2e] via-[#152238] to-[#192841]'
            : 'bg-[#E7D4AB]'
        }`}
      >
        <div className="max-w-7xl mx-auto p-4 min-h-screen flex flex-col">
          
          {/* HEADER */}
          <div className={`rounded-2xl p-6 mb-4 backdrop-blur-xl ${
            darkMode
              ? 'bg-gradient-to-r from-[#152238]/90 to-[#192841]/90 border-2 border-[#203354] shadow-[0_0_40px_rgba(32,51,84,0.5)]'
              : 'bg-[#a36a13] border-2 border-[#AF6E4D] shadow-2xl'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className={`w-16 h-16 rounded-full flex items-center justify-center text-4xl shadow-lg ${
                  darkMode ? 'bg-[#203354]/50' : 'bg-white/30'
                } backdrop-blur-lg`}>
                  🦚
                </div>
                <div>
                  <h1 className={`text-3xl font-bold flex items-center gap-2 ${
                    darkMode ? 'text-[#F4F4DB]' : 'text-white'
                  }`}>
                    KanhAI
                    <Sparkles className="w-6 h-6" />
                  </h1>
                  <p className={`text-sm ${darkMode ? 'text-[#E7D4AB]' : 'text-white/90'}`}>
                    Your Vrindavan Companion & Guide
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <button
                  onClick={() => setShowSettings(!showSettings)}
                  className={`p-3 rounded-full backdrop-blur-lg transition ${
                    darkMode 
                      ? 'bg-[#203354]/50 hover:bg-[#203354]/70 text-[#F4F4DB]' 
                      : 'bg-white/20 hover:bg-white/30 text-white'
                  }`}
                >
                  <Settings className="w-5 h-5" />
                </button>
              </div>
            </div>

            {showSettings && (
              <div className={`mt-4 p-4 backdrop-blur-lg rounded-xl ${
                darkMode ? 'bg-[#192841]/50 border-2 border-[#203354]' : 'bg-white/80 border-2 border-[#CBA271]'
              }`}>
                <h3 className={`font-semibold mb-3 ${darkMode ? 'text-[#F4F4DB]' : 'text-black'}`}>
                  Session Information
                </h3>
                <div className={`space-y-2 text-sm ${darkMode ? 'text-[#E7D4AB]' : 'text-black'}`}>
                  <p> Topics: {(userContext.topics_discussed || []).join(", ") || "None yet"}</p>
                  <p> Emotional State: {userContext.emotional_state}</p>
                  <p> Started: {new Date(userContext.session_start).toLocaleString()}</p>
                  <button
                    onClick={clearSession}
                    className="mt-3 px-4 py-2 bg-red-500/80 hover:bg-red-600 text-white rounded-lg transition"
                  >
                    Reset Session
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* CHAT */}
          <div className={`flex-1 rounded-2xl overflow-hidden flex flex-col ${
            darkMode
              ? 'bg-[#152238]/40 backdrop-blur-xl border-2 border-[#203354] shadow-[0_0_40px_rgba(32,51,84,0.4)]'
              : 'bg-white border-2 border-[#CBA271] shadow-2xl'
          }`}>
            <div className="flex-1 overflow-y-auto p-6 space-y-6">
              
              {messages.map((msg) => (
                <div
                  key={msg.id}
                  className={`flex ${msg.type === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div className="max-w-2xl">
                    
                    {msg.type === "user" && (
                      <div className={`rounded-2xl rounded-tr-sm p-4 ${
                        darkMode
                          ? 'bg-gradient-to-r from-[#192841] to-[#203354] text-[#F4F4DB] border-2 border-[#203354] shadow-[0_0_20px_rgba(32,51,84,0.4)]'
                          : 'bg-[#CBA271] text-white border-2 border-[#a97c66] shadow-lg'
                      }`}>
                        <p className="whitespace-pre-wrap">{msg.text}</p>
                        <p className={`text-xs mt-2 ${darkMode ? 'text-[#CBA271]' : 'text-white/80'}`}>
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    )}

                    {msg.type === "krishna" && (
                      <div className={`rounded-2xl rounded-tl-sm p-5 ${
                        darkMode
                          ? 'bg-gradient-to-br from-[#192841]/70 to-[#152238]/70 backdrop-blur-sm border-2 border-[#203354] shadow-[0_0_25px_rgba(32,51,84,0.4)]'
                          : 'bg-white border-2 border-[#CBA271] shadow-lg'
                      }`}>
                        <div className="flex items-start gap-3 mb-3">
                          <div className="text-2xl"></div>
                          <div className="flex-1">
                            <p className={`font-semibold ${darkMode ? 'text-[#F4F4DB]' : 'text-[#26395c]'}`}>
                              Kanha
                            </p>
                          </div>
                        </div>

                        {msg.verse && (
                          <div className={`mb-4 p-4 rounded-xl border-l-4 ${
                            darkMode
                              ? 'bg-[#0f1a2e]/30 border-[#CBA271] shadow-inner'
                              : 'bg-[#F4F4DB] border-[#AF6E4D] shadow-sm'
                          }`}>
                            <div className="flex items-center gap-2 mb-2">
                              <BookOpen className={`w-4 h-4 ${darkMode ? 'text-[#CBA271]' : 'text-[#152238]'}`} />
                              <span className={`text-xs font-semibold ${darkMode ? 'text-[#CBA271]' : 'text-[#152238]'}`}>
                                Bhagavad Gita {msg.verse.chapter}.{msg.verse.verse_num}
                              </span>
                            </div>
                            <p className={`text-sm italic mb-2 ${darkMode ? 'text-[#E7D4AB]' : 'text-[#0f1a2e]'}`}>
                              {msg.verse.verse}
                            </p>
                            <p className={`text-xs ${darkMode ? 'text-[#BDB865]' : 'text-[#152238]'}`}>
                              {msg.verse.translation}
                            </p>
                          </div>
                        )}

                        <p className={`whitespace-pre-wrap leading-relaxed ${darkMode ? 'text-[#E7D4AB]' : 'text-[#152238]'}`}>
                          {msg.text}
                        </p>

                        {msg.suggestions && (
                          <div className={`mt-4 pt-4 border-t-2 ${darkMode ? 'border-[#203354]' : 'border-[#CBA271]'}`}>
                            <p className={`text-xs font-semibold mb-2 ${darkMode ? 'text-[#BDB865]' : 'text-[#152238]'}`}>
                              🌿 Suggested paths:
                            </p>
                            <div className="flex flex-wrap gap-2">
                              {msg.suggestions.map((sugg, idx) => (
                                <button
                                  key={idx}
                                  onClick={() => handleSuggestionClick(sugg)}
                                  className={`text-xs px-3 py-1.5 rounded-full transition ${
                                    darkMode
                                      ? 'bg-[#152238]/60 hover:bg-[#192841]/60 text-[#F4F4DB] border-2 border-[#203354]'
                                      : 'bg-[#F4F4DB] hover:bg-[#E7D4AB] text-[#0f1a2e] border-2 border-[#CBA271]'
                                  }`}
                                >
                                  {sugg}
                                </button>
                              ))}
                            </div>
                          </div>
                        )}

                        <p className={`text-xs mt-3 ${darkMode ? 'text-[#BDB865]' : 'text-[#192841]'}`}>
                          {new Date(msg.timestamp).toLocaleTimeString()}
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className={`max-w-2xl rounded-2xl p-5 ${
                    darkMode 
                      ? 'bg-[#152238]/50 border-2 border-[#203354] shadow-[0_0_20px_rgba(32,51,84,0.3)]' 
                      : 'bg-white border-2 border-[#CBA271] shadow-lg'
                  }`}>
                    <div className="flex items-center gap-3">
                      <Loader2 className={`w-5 h-5 animate-spin ${darkMode ? 'text-[#CBA271]' : 'text-[#152238]'}`} />
                      <p className={darkMode ? 'text-[#E7D4AB]' : 'text-[#152238]'}>Kanha is thinking...</p>
                    </div>
                  </div>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* INPUT */}
            <div className={`p-4 border-t-2 ${
              darkMode
                ? 'border-[#203354] bg-[#152238]/50'
                : 'border-[#CBA271] bg-white/80'
            }`}>
              <div className="flex gap-3">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
                  placeholder="Speak your heart to Kanha..."
                  disabled={isLoading}
                  className={`flex-1 px-5 py-3 rounded-xl focus:outline-none focus:ring-2 transition ${
                    darkMode
                      ? 'bg-[#0f1a2e] text-[#F4F4DB] placeholder-[#BDB865] focus:ring-[#203354] border-2 border-[#192841] shadow-inner'
                      : 'bg-white text-[#0f1a2e] placeholder-[#BDB865] focus:ring-[#CBA271] border-2 border-[#CBA271] shadow-sm'
                  } disabled:opacity-50`}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !input.trim()}
                  className={`px-6 py-3 rounded-xl font-semibold transition disabled:opacity-75 ${
                    darkMode
                      ? 'bg-gradient-to-r from-[#152238] to-[#192841] hover:from-[#192841] hover:to-[#203354] text-[#F4F4DB] border-2 border-[#203354] shadow-[0_0_20px_rgba(32,51,84,0.4)]'
                      : ' hover:bg-[#203354]  bg-[#621f0a] text-white border-2  shadow-lg'
                  }`}
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>

          {/* FOOTER */}
          <div className={`text-center mt-4 text-sm ${darkMode ? 'text-[#ccc89a]' : 'text-[#152238]'}`}>
            <p className="flex items-center justify-center gap-2">
              Made with <Heart className="w-4 h-4 text-red-500 fill-red-500" /> for Krishna lovers
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KrishnaAI;