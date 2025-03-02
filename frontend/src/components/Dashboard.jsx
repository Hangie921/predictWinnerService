import { useState } from "react";
import api from '../api'
// import { useNavigate } from "react-router-dom";
import LoadingIndicator from "./LoadingIndicator";
import "../styles/Dashboard.scss"
import Card from "./Card";
// import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";


function Dashboard() {
    const [cards, setCards] = useState([])
    const [isLoading, setLoading] = useState(false)
    const [date, setDate] = useState("2024-08-01")
    const [diffWeight, setDiffWeight] = useState(1.5)
    const [l10Weight, setL10Weight] = useState(1.4)
    const [homeAwayWeight, setHomeAwayWeight] = useState(1.3)
    const [handedWeight, setHandedWeight] = useState(1.2)
    const [overallWeight, setOverallWeight] = useState(0.1)

    const fetchData = async () => {
        setLoading(true)
        try {
            const res = await api.get("prediction?date=2024-08-01&diff_weight=1.5&l10_weight=1.4&home_away_weight=1.3&handed_weight=1.2&overall_weight=0.1")
            console.table(res.data)
            console.log('res.data is array', Array.isArray(res.data))
            setCards(res.data)
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }
    const getCardRows = function () {
        let tmp = Array.from(cards)
        let ret = []
        while (tmp.length) ret.push(tmp.splice(0, 3))
        return ret
    }
    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <button onClick={fetchData}>Fetch Data</button>
            {isLoading && <LoadingIndicator />}
            <div className="cards-container flex flex-wrap flex-justify-between flex-column">
                {getCardRows().map((row, rIdx) => {
                    console.log('ridx', rIdx)
                    const isLastRow = rIdx === row.length - 1
                    const rowClassName = isLastRow ? "card-row last flex flex-justify-start" : "card-row flex flex-justify-between"
                    return (
                        <div className={rowClassName} key={rIdx} >
                            {row.map((card, cIdx) => {
                                return <Card key={cIdx} index={cIdx + 1} isLast={cIdx === row.length - 1} data={card} />
                            })}
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default Dashboard