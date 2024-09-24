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
        <Dropdown.Item onClick={() => changeLanguage('gr')}>Greek</Dropdown.Item>
        {/* Add more languages as needed */}
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default LanguageSwitcher;
