import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "../pages/Home.jsx";
import AuthPage from "../pages/AuthPage.jsx";
import Login from "../pages/Login.jsx";
import Register from "../pages/Register.jsx";

export default function AppRoutes() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} /> 
        <Route path="/auth" element={<AuthPage />} />
        <Route path="/auth/login" element={<Login />} />
        <Route path="/auth/register" element={<Register />} />      
      </Routes>
    </Router>
  );
}
