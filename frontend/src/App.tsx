import { Toaster } from "react-hot-toast";
import { Route, Routes } from "react-router";
import Navbar from "./components/Navbar";
import Home from "./pages/home";
import PropertiesPage from "./pages/properties";

function Router() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/properties" element={<PropertiesPage />} />
    </Routes>
  );
}

function App() {
  return (
    <>
      <Toaster position="top-right" />
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          <Router />
        </main>
      </div>
    </>
  );
}

export default App;
