import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Import translation files for each language
import enTranslations from './i18n/locales/en/translation.json';
import grTranslations from './i18n/locales/gr/translation.json';
import esTranslations from './i18n/locales/es/translation.json';
import frTranslations from './i18n/locales/fr/translation.json';
import deTranslations from './i18n/locales/de/translation.json';
import itTranslations from './i18n/locales/it/translation.json';
import ruTranslations from './i18n/locales/ru/translation.json';
import zhTranslations from './i18n/locales/zh/translation.json';
import jaTranslations from './i18n/locales/ja/translation.json';
import ptTranslations from './i18n/locales/pt/translation.json';

// Initialize i18n
i18n
  .use(LanguageDetector)  // Automatically detect user language
  .use(initReactI18next)  // Bind i18n to React
  .init({
    resources: {
      en: { translation: enTranslations },
      gr: { translation: grTranslations },
      es: { translation: esTranslations },
      fr: { translation: frTranslations },
      de: { translation: deTranslations },
      it: { translation: itTranslations },
      ru: { translation: ruTranslations },
      zh: { translation: zhTranslations },
      ja: { translation: jaTranslations },
      pt: { translation: ptTranslations },
    },
    fallbackLng: 'en',  // Fallback language if none is detected
    detection: {
      order: ['localStorage', 'navigator', 'htmlTag'],  // Detect order
      caches: ['localStorage'],  // Cache language selection
    },
    interpolation: {
      escapeValue: false,  // React already protects from XSS
    },
  });

export default i18n;
