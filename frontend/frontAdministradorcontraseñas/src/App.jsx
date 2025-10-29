import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
// import Dashboard from "./pages/Dashboard"; // para cuando lo tengas

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        {/* <Route path="/dashboard" element={<Dashboard />} /> */}
        <Route path="*" element={<Navigate to="/" />} /> {/* redirige a login si ruta no existe */}
      </Routes>
    </Router>
  );
}

export default App;
