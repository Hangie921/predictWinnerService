import Dashboard from "../components/Dashboard"
import Header from "../components/Header"


function Home() {
  return (
    <div>
      <Header />
      <h1 className="page-title">Predict the Winner</h1>
      <Dashboard page="home" />
    </div>
  )
}

export default Home