import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'

import '@mantine/core/styles.css';
import { MantineProvider, createTheme } from '@mantine/core';

const theme = createTheme({
  primaryColor: 'pink',
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
  defaultGradient: { from: 'pink', to: 'gold', deg: 0 },
});

createRoot(document.getElementById('root')).render(
  <MantineProvider theme={theme}>
    <StrictMode>
      <App />
    </StrictMode>
  </MantineProvider>,
)
