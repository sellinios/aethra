// src/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files for each language
import enTranslations from './i18n/locales/en/translation.json';
import elTranslations from './i18n/locales/el/translation.json';
import esTranslations from './i18n/locales/es/translation.json';
import frTranslations from './i18n/locales/fr/translation.json';
import deTranslations from './i18n/locales/de/translation.json';
import itTranslations from './i18n/locales/it/translation.json';
import ruTranslations from './i18n/locales/ru/translation.json';
import zhTranslations from './i18n/locales/zh/translation.json';
import jaTranslations from './i18n/locales/ja/translation.json';
import ptTranslations from './i18n/locales/pt/translation.json';

// Initialize i18n
// src/i18n.ts
i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: {
      en: { translation: enTranslations },
      el: { translation: elTranslations },
      es: { translation: esTranslations },
      fr: { translation: frTranslations },
      de: { translation: deTranslations },
      it: { translation: itTranslations },
      ru: { translation: ruTranslations },
      zh: { translation: zhTranslations },
      ja: { translation: jaTranslations },
      pt: { translation: ptTranslations },
    },
    fallbackLng: 'el', // Default to Greek if no language is detected
    supportedLngs: ['en', 'el', 'es', 'fr', 'de', 'it', 'ru', 'zh', 'ja', 'pt'],
    detection: {
      order: ['localStorage', 'cookie', 'navigator', 'htmlTag'],
      caches: ['localStorage', 'cookie'],
      lookupLocalStorage: 'i18nextLng',
      lookupCookie: 'i18next',
    },
    interpolation: {
      escapeValue: false,
    },
    debug: false,
    // Override the language detection for 'en-*' to be treated as 'en'
    react: {
      useSuspense: false,
    },
    lng: i18n.language && i18n.language.startsWith('en') ? 'en' : i18n.language,
  });


export {};
