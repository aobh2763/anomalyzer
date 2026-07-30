import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import '@mantine/core/styles.css';
import { MantineProvider } from '@mantine/core';

import { BrowserRouter, Routes, Route } from "react-router";
import LandingPage from './pages/LandingPage.jsx';
import EvaluationPage from './pages/EvaluationPage.jsx';
import LogPage from './pages/LogPage.jsx';
import ModelPage from './pages/ModelPage.jsx';
import Layout from './components/Layout.jsx';
import AboutPage from './pages/AboutPage.jsx';
import theme from './theme.jsx';

createRoot(document.getElementById('root')).render(
  <MantineProvider theme={theme} defaultColorScheme="dark">
    <StrictMode>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<LandingPage />} />
            <Route path="models" element={<ModelPage />} />
            <Route path="logs" element={<LogPage />} />
            <Route path="evaluation" element={<EvaluationPage />} />
            <Route path="about" element={<AboutPage />} />
          </Route>
        </Routes>
      </BrowserRouter>,
    </StrictMode>
  </MantineProvider>
)
