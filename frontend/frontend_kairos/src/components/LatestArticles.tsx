import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Typography } from 'antd';
import { useTranslation } from 'react-i18next';
import i18n from 'i18next';  // Import the i18n instance

const { Title } = Typography;

interface Article {
  title: string;
  slug: string;
  summary: string;
}

const LatestArticles: React.FC = () => {
  const { t } = useTranslation();
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    const fetchArticles = async () => {
      try {
        const apiUrl = `${process.env.REACT_APP_API_URL}/${i18n.language}/api/news/`;  // Use i18n.language to fetch the correct language version
        const response = await fetch(apiUrl);
        const data = await response.json();
        setArticles(data.slice(0, 3)); // Get the 3 latest articles
      } catch (err) {
        console.error('Error fetching articles:', err);
      }
    };

    fetchArticles();
  }, [i18n.language]);  // Re-fetch articles when the language changes

  return (
    <>
      <Row className="justify-content-center mt-5">
        <Col xs={12}>
          <Title level={3}>{t('latestArticles')}</Title>
        </Col>
      </Row>
      <Row>
        {articles.map((article) => (
          <Col key={article.slug} xs={12} md={4}>
            <Card title={article.title} bordered={false}>
              <p>{article.summary}</p>
              <a href={`/news/${article.slug}`}>{t('readMore')}</a>
            </Card>
          </Col>
        ))}
      </Row>
    </>
  );
};

export default LatestArticles;
