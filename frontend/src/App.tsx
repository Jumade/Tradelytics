import React from 'react';
import './App.css';

import {BrowserRouter, Route, Routes} from "react-router-dom";
import PortfolioPage from "./pages/PortfolioPage"
import Layout from "./components/Layout";
import LoginPage from "./pages/LoginPage";
import PrivateRoute from "./components/PrivateRoute";
import AccountSettingsPage from './pages/AccountSettingsPage';

function App() {
  return (
    <div className="App">
        <React.Suspense fallback={<div>Loading...</div>}>
      
        <BrowserRouter>
            <Routes>
                <Route element={<Layout />}>
                    <Route path="/" element={<PrivateRoute><PortfolioPage /></PrivateRoute>} />
                    <Route path="/settings" element={<PrivateRoute><AccountSettingsPage /></PrivateRoute>} />

                    <Route path="/login" element={<LoginPage />} />
                </Route>
            </Routes>

        </BrowserRouter>
        </React.Suspense>
    </div>
  );
}

export default App;
