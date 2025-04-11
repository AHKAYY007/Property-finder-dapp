import { BrowserRouter, Route, Routes } from "react-router";
import { Toaster } from "react-hot-toast";
import Home from "./pages/home";
import Navbar from "./components/Navbar";
import PropertiesPage from "./pages/properties";

function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/properties" element={<PropertiesPage />} />
      </Routes>
    </BrowserRouter>
  );
}

function App() {
  <>
    <Toaster position="top-right" />
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        <Router />
      </main>
    </div>
  </>;
}

export default App;
