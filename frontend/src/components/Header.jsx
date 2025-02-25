import React from 'react';
import '../styles/Header.scss';

function HeaderButton(props) {
  return (
    <div className="HeaderButton">
      <a href={props.url}>{props.name}</a>
    </div>
  )
}

function Header() {
  return (
    <header className="Header">
      <HeaderButton url="/" name="Home" />
      <HeaderButton url="/backtest" name="BackTest" />
      <HeaderButton url="/logout" name="Logout" />
    </header>
  );
};

export default Header;
