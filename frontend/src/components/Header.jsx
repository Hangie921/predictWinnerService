import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.scss';

function Header () {
  return (
    <header className="Header">
      <nav>
        <ul>
          <li>
            <Link to="/">Home</Link>
          </li>
          <li>
            <Link to="/backtest">BackTest</Link>
          </li>
          <li>
            <Link to="/logout">Logout</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
