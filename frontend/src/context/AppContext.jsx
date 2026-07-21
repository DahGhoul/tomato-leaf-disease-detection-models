import React, { createContext, useContext, useState, useEffect } from 'react';
import { UI_TEXTS } from '../utils/translations';

const AppContext = createContext();

export function AppProvider({ children }) {
  const [lang, setLang] = useState('es'); // 'es' or 'en'
  const [theme, setTheme] = useState('dark'); // 'dark' or 'light'

  // Apply theme to HTML root
  useEffect(() => {
    const root = window.document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');
  const toggleLang = () => setLang(prev => prev === 'es' ? 'en' : 'es');

  const t = UI_TEXTS[lang];

  return (
    <AppContext.Provider value={{ lang, theme, toggleTheme, toggleLang, t }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext() {
  return useContext(AppContext);
}
