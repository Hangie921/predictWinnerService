import "../styles/BackTest.scss"
import Dashboard from "../components/Dashboard"
import Header from "../components/Header"


function BackTest() {
  return (
    <div>
      <Header />
      <h1 className="page-title">BackTest</h1>
      <Dashboard page="backtest" />
    </div>
  )
}

export default BackTest