// src/i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(LanguageDetector) // Detects user language
  .use(initReactI18next)  // Passes i18n instance to react-i18next
  .init({
    resources: {
      en: {
        translation: {
          home: 'Home',
          about: 'About',
          contact: 'Contact',
          geography: 'Geography',
          municipalities: 'Municipalities',
          regions: 'Regions',
          login: 'Login',
          register: 'Register',
          // ... other translations
        },
      },
      gr: {
        translation: {
          home: 'Αρχική',
          about: 'Σχετικά',
          contact: 'Επικοινωνία',
          geography: 'Γεωγραφία',
          municipalities: 'Δήμοι',
          regions: 'Περιφέρειες',
          login: 'Σύνδεση',
          register: 'Εγγραφή',
          // ... other translations
        },
      },
      // Add more languages as needed
    },
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false, // React already protects from XSS
    },
  });

export default i18n;
