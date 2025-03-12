import { useState } from "react";
import DashboardCardView from "./DashboardCardView.jsx";
import DashboardAnalysisView from "./DashboardAnalysisView.jsx";
import ParameterSelector from './ParameterSelector.jsx';
import LoadingIndicator from "./LoadingIndicator";
import { dayjs, easternTimeZone } from "../timeAndDay.js"
import api from '../api'

import "../styles/Dashboard.scss"
import "../styles/Button.scss"

const defaultStartDateValue = "2024-08-01"
const defaultEndDateValue = "2024-08-10"
const dateFormat = "YYYY-MM-DD"

const defaultDiffWeight = 1
const defaultL10Weight = 1
const defaultHomeAwayWeight = 1
const defaultHandedWeight = 1
const defaultOverallWeight = 1

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

function Dashboard({ page }) {
    console.log('page', page)
    const [cards, setCards] = useState([])
    const [analysis, setAnalysis] = useState({})
    const [isLoading, setLoading] = useState(false)
    const [startDate, setStartDate] = useState(dayjs.tz(defaultStartDateValue, easternTimeZone))
    const [endDate, setEndDate] = useState(dayjs.tz(defaultEndDateValue, easternTimeZone))
    const [diffWeight, setDiffWeight] = useState(defaultDiffWeight)
    const [l10Weight, setL10Weight] = useState(defaultL10Weight)
    const [homeAwayWeight, setHomeAwayWeight] = useState(defaultHomeAwayWeight)
    const [handedWeight, setHandedWeight] = useState(defaultHandedWeight)
    const [overallWeight, setOverallWeight] = useState(defaultOverallWeight)

    const fetchData = async () => {
        if (page === 'home') {
            setLoading(true)
            setCards([])
            try {
                const res = await api.get(`prediction?date=${startDate.format(dateFormat)}&diff_weight=${diffWeight}&l10_weight=${l10Weight}&home_away_weight=${homeAwayWeight}&handed_weight=${handedWeight}&overall_weight=${overallWeight}`)
                console.table(res.data)
                setCards(res.data)
            } catch (error) {
                alert(error)
            } finally {
                setLoading(false)
            }
            return
        }
        setLoading(true)
        setAnalysis({})
        try {
            const res = await api.get(`backtest?start_date=${startDate.format(dateFormat)}&end_date=${endDate.format(dateFormat)}&diff_weight=${diffWeight}&l10_weight=${l10Weight}&home_away_weight=${homeAwayWeight}&handed_weight=${handedWeight}&overall_weight=${overallWeight}`)
            console.table(res.data)
            setAnalysis(res.data)
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    }

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

    let parameterRequirement = {
        page,
        minDate,
        maxDate,
        startDate,
        endDate,
        weights,
        setStartDate,
        setEndDate,
        setDiffWeight,
        setL10Weight,
        setHomeAwayWeight,
        setHandedWeight,
        setOverallWeight
    }

    const renderResultView = function () {
        return page === 'home' ? (<DashboardCardView cards={cards} />) : (<DashboardAnalysisView />)
    }

    return (
        <div className="dashboard">
            <ParameterSelector requirement={parameterRequirement}
                page={page}
                startDate={startDate}
                minDate={minDate}
                maxDate={maxDate}
                setStartDate={setStartDate}
                setEndDate={setEndDate}
            />
            <button className="btn" onClick={fetchData}>Get the result</button>
            {isLoading && <LoadingIndicator />}
            {renderResultView()}
        </div>
    )
}

export default Dashboard