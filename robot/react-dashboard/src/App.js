import React, {Component} from "react";
import {BrowserRouter, Route, Routes, Navigate} from 'react-router-dom';

import './App.css';
import Main from "./components/main/Main";
import Detail from "./components/detail/Detail";
import Login from "./components/login/Login";

function App() {
    const UnAuthorized = ({
        children,
    }) => {
        if (! localStorage.getItem('jwtToken') ) {
            return <Navigate to='/login' replace />;
        }
        return children;
    };

    const Authorized = ({
        children,
    }) => {
        if (localStorage.getItem('jwtToken') ) {
            return <Navigate to='/' replace />;
        }
        return children;
    };

  return (
    <div className="App">
      <BrowserRouter>
          <Routes>
              <Route path="/" element={<UnAuthorized><Main/></UnAuthorized>} />
              <Route path="/detail/:id" element={<UnAuthorized><Detail/></UnAuthorized>} />
              <Route path="/login" element={<Authorized><Login/></Authorized>} />
          </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
