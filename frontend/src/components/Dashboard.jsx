import { useState } from "react";
import api from '../api'
// import { useNavigate } from "react-router-dom";
import LoadingIndicator from "./LoadingIndicator";
import "../styles/Dashboard.scss"
import Card from "./Card";
// import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";


function Dashboard() {
    const [data, setData] = useState([])
    const [isLoading, setLoading] = useState(false)

    const fetchData = async () => {
        setLoading(true)
        try {
            const res = await api.get("dashboard")
            setData(res.data)
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }
    const cards = [
        { index: "1" },
        { index: "2" },
        { index: "3" },
        { index: "4" },
        { index: "5" },
        // { index: "6" },
    ]
    const getRowCards = function (from) {
        let ret = []
        while (from.length) ret.push(from.splice(0, 3))
        return ret
    }
    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <button onClick={fetchData}>Fetch Data</button>
            {isLoading && <LoadingIndicator />}
            <div className="cards-container flex flex-wrap flex-justify-between flex-column">
                {getRowCards(cards).map((row, rIdx) => {
                    console.log('ridx', rIdx)
                    const isLastRow = rIdx === row.length - 1
                    const rowClassName = isLastRow ? "card-row last flex flex-justify-start" : "card-row flex flex-justify-between"
                    return (
                        <div className={rowClassName} key={rIdx} >
                            {row.map((card, cIdx) => {
                                return <Card key={cIdx} index={card.index} isLast={cIdx === row.length - 1} />
                            })}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

// function Form({ route, method }) {
//     const [username, setUsername] = useState("")
//     const [password, setPassword] = useState("")
//     const [isLoading, setLoading] = useState(false)
//     const navigate = useNavigate()

//     const name = method === "login" ? "Login" : "Register"

//     const handleSubmit = async (e) => {
//         setLoading(true)
//         e.preventDefault()

//         try {
//             const res = await api.post(route, { username, password })
//             if (method == "login") {
//                 localStorage.setItem(ACCESS_TOKEN, res.data.access)
//                 localStorage.setItem(REFRESH_TOKEN, res.data.refresh)
//                 navigate("/")
//             } else {
//                 navigate("login")
//             }
//         } catch (error) {
//             alert(error)
//         } finally {
//             setLoading(false)
//         }
//     }

//     return (
//         <form onSubmit={handleSubmit}>
//             <h1>{name}</h1>
//             <input
//                 className="form-input"
//                 type="text"
//                 value={username}
//                 onChange={(e) => setUsername(e.target.value)}
//                 placeholder="Username"
//             />
//             <input
//                 className="form-input"
//                 type="password"
//                 value={password}
//                 onChange={(e) => setPassword(e.target.value)}
//                 placeholder="Password"
//             />
//             {isLoading && <LoadingIndicator />}
//             <button className="form-button" type="submit">
//                 {name}
//             </button>
//         </form>
//     )
// }

export default Dashboard