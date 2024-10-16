// src/components/LanguageSwitcher.tsx
import React from 'react';
import { Dropdown } from 'react-bootstrap';
import { useTranslation } from 'react-i18next';

const LanguageSwitcher: React.FC = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  const currentLanguage = i18n.language || 'en';

  return (
    <Dropdown className="language-switcher">
      <Dropdown.Toggle variant="outline-light" id="language-dropdown">
        {currentLanguage.toUpperCase()}
      </Dropdown.Toggle>
      <Dropdown.Menu>
        <Dropdown.Item onClick={() => changeLanguage('en')}>English</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('el')}>Ελληνικά (Greek)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('es')}>Español (Spanish)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('fr')}>Français (French)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('de')}>Deutsch (German)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('it')}>Italiano (Italian)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('ru')}>Русский (Russian)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('zh')}>中文 (Chinese)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('ja')}>日本語 (Japanese)</Dropdown.Item>
        <Dropdown.Item onClick={() => changeLanguage('pt')}>Português (Portuguese)</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default LanguageSwitcher;
