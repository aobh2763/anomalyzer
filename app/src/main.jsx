import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import '@mantine/core/styles.css';
import { MantineProvider, createTheme } from '@mantine/core';

import { BrowserRouter, Routes, Route } from "react-router";
import LandingPage from './pages/LandingPage.jsx';
import EvaluationPage from './pages/EvaluationPage.jsx';
import LogPage from './pages/LogPage.jsx';
import ModelPage from './pages/ModelPage.jsx';
import Layout from './components/Layout.jsx';
import AboutPage from './pages/AboutPage.jsx';

const theme = createTheme({
  primaryColor: 'pink',
  forceColorScheme: 'dark',
  colors: {
    pink: [
      '#fff0f6', '#ffdeeb', '#fcc2d7', '#faa2c1', '#f783ac',
      '#f06595', '#e64980', '#d6336c', '#c2255c', '#a61e4d',
    ],
    gold: [
      '#fff9db', '#fff3bf', '#ffec99', '#ffe066', '#ffd43b',
      '#fcc419', '#fab005', '#f08c00', '#e67700', '#d9480f',
    ],
  },
});

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
