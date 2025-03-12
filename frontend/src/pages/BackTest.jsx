import "../styles/BackTest.scss"
import Dashboard from "../components/Dashboard"

function BackTest() {
  return (
    <div>
      <h1 className="page-title">BackTest</h1>
      <Dashboard page="backtest" />
    </div>
  )
}

export default BackTest