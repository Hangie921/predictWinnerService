import NumberInput from './NumberInput'
import { useState } from "react";
import api from '../api'
import LoadingIndicator from "./LoadingIndicator";
import "../styles/Dashboard.scss"
import "../styles/Button.scss"
import Card from "./Card";
import DatePicker from "./DatePicker"
import dayjs from "dayjs"
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone"
dayjs.extend(utc)
dayjs.extend(timezone)

const easternTimeZone = "America/New_York"
const dateFormat = "YYYY-MM-DD"
const defaultDiffWeight = 1
const defaultL10Weight = 1
const defaultHomeAwayWeight = 1
const defaultHandedWeight = 1
const defaultOverallWeight = 1
const defaultDateValue = "2024-08-01"

let minDate = dayjs.tz('2024-01-01', easternTimeZone)
let maxDate = dayjs.tz('2025-12-31', easternTimeZone)

const fetchSupportedDate = async () => {
    try {
        const res = await api.get(`supportedDate`)
        console.log('res', res)
        minDate = dayjs(res.data[0].startDate)
        maxDate = dayjs(res.data[0].endDate)
    } catch (error) {
        alert(error)
    } finally {
        // setLoading(false)
    }
}
fetchSupportedDate()

function Dashboard() {
    const [cards, setCards] = useState([])
    const [isLoading, setLoading] = useState(false)
    const [date, setDate] = useState(dayjs.tz(defaultDateValue, easternTimeZone))
    const [diffWeight, setDiffWeight] = useState(defaultDiffWeight)
    const [l10Weight, setL10Weight] = useState(defaultL10Weight)
    const [homeAwayWeight, setHomeAwayWeight] = useState(defaultHomeAwayWeight)
    const [handedWeight, setHandedWeight] = useState(defaultHandedWeight)
    const [overallWeight, setOverallWeight] = useState(defaultOverallWeight)

    const weights = [{
        "name": 'Overall Weight',
        "setFunction": setOverallWeight,
        "defaultValue": defaultOverallWeight,
    }, {
        "name": 'Home/Away Weight',
        "setFunction": setHomeAwayWeight,
        "defaultValue": defaultHomeAwayWeight,
    }, {
        "name": 'Handed Weight',
        "setFunction": setHandedWeight,
        "defaultValue": defaultHandedWeight,
    }, {
        "name": 'Last 10 Weight',
        "setFunction": setL10Weight,
        "defaultValue": defaultL10Weight,
    }, {
        "name": 'Diff Weight',
        "setFunction": setDiffWeight,
        "defaultValue": defaultDiffWeight,
    }]


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
        return ret
    }

    return (
        <div className="dashboard">
            <h1>Predict the Winner</h1>
            <div className="parameter-section flex flex-justify-between">
                <div className="date-picker-section">
                    {/* <span>
                        {date.toString()}
                    </span> */}
                    <DatePicker
                        date={date}
                        onChange={(newVal) => { setDate(newVal) }}
                        minDate={minDate}
                        maxDate={maxDate}
                    />
                </div>
                <div className="weight-input-section flex flex-justify-between">
                    {
                        weights.map((weight, wIdx) => {
                            return (
                                <NumberInput
                                    className="flex weight-input flex-column"
                                    name={weight.name}
                                    defaultValue={weight.defaultValue}
                                    onValueChange={weight.setFunction}
                                    key={wIdx}
                                />
                            )
                        })
                    }
                </div>
            </div>
            <button className="btn" onClick={fetchData}>Get the result</button>
            {isLoading && <LoadingIndicator />}
            <div className="cards-container flex flex-wrap flex-justify-between flex-column">
                {
                    getCardRows().map((row, rIdx) => {
                        console.log('ridx', rIdx)
                        const isLastRow = rIdx === getCardRows().length - 1
                        const rowClassName = isLastRow ? "card-row flex flex-justify-between" : "card-row flex flex-justify-between"
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