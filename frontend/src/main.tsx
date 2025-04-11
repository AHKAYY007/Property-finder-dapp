import { SuiClientProvider, WalletProvider } from "@mysten/dapp-kit";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import "./index.css";

// NOTE YOU'D NEED TO SEE HOW TO SETUP DAPP-KIT PROPERLY
// LINK https://www.npmjs.com/package/@mysten/dapp-kit

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <SuiClientProvider>
      <WalletProvider>
        <App />
      </WalletProvider>
    </SuiClientProvider>
  </StrictMode>
);
