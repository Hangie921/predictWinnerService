import { useState } from "react";
import api from '../api'
// import { useNavigate } from "react-router-dom";
import LoadingIndicator from "./LoadingIndicator";
import "../styles/Dashboard.scss"
import Card from "./Card";
// import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import DatePicker from "./DatePicker"
import dayjs from "dayjs"

const dateFormat = "YYYY-MM-DD"
const defaultDiffWeight = 1
const defaultL10Weight = 1
const defaultHomeAwayWeight = 1
const defaultHandedWeight = 1
const defaultOverallWeight = 1

function Dashboard() {
    const [cards, setCards] = useState([])
    const [isLoading, setLoading] = useState(false)
    const [date, setDate] = useState(dayjs('2024-08-01'))
    const [diffWeight, setDiffWeight] = useState(defaultDiffWeight)
    const [l10Weight, setL10Weight] = useState(defaultL10Weight)
    const [homeAwayWeight, setHomeAwayWeight] = useState(defaultHomeAwayWeight)
    const [handedWeight, setHandedWeight] = useState(defaultHandedWeight)
    const [overallWeight, setOverallWeight] = useState(defaultOverallWeight)

    const fetchData = async () => {
        setLoading(true)
        setCards([])
        try {
            const res = await api.get(`prediction?date=${date.format(dateFormat)}&diff_weight=${diffWeight}&l10_weight=${l10Weight}&home_away_weight=${homeAwayWeight}&handed_weight=${handedWeight}&overall_weight=${overallWeight}`)
            console.table(res.data)
            setCards(res.data)
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }
    const getCardRows = function () {
        let tmp = Array.from(cards)
        if (tmp.length % 3 === 2) tmp.push({ gameID: 'fake' })
        let ret = []
        while (tmp.length) ret.push(tmp.splice(0, 3))

        console.log(`[getCardRows] is ${ret.length}`)
        return ret
    }
    const handleDateChange = function (newVal) {
        console.log(`[handleDateChange] ${newVal}`)
        setDate(newVal)
    }

    return (
        <div className="dashboard">
            <h1>Dashboard</h1>
            <div className="datePicker">
                <DatePicker onChange={handleDateChange} date={date} />
            </div>
            <button onClick={fetchData}>Fetch Data</button>
            {isLoading && <LoadingIndicator />}
            <div className="cards-container flex flex-wrap flex-justify-between flex-column">
                {
                    getCardRows().map((row, rIdx) => {
                        console.log('ridx', rIdx)
                        const isLastRow = rIdx === getCardRows().length - 1
                        const rowClassName = isLastRow ? "card-row last flex flex-justify-between" : "card-row flex flex-justify-between"
                        return (
                            <div className={rowClassName} key={rIdx} >
                                {row.map((card, cIdx) => {
                                    return <Card key={cIdx} index={cIdx + 1} isLast={cIdx === row.length - 1} data={card} />
                                })}
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default Dashboard