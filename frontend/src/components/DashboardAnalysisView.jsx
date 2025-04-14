import { toPercentageStr, round } from "../math"
import "../styles/DashboardAnalysisView.scss"

function getTeamLogoURL(id) {
    return `https://www.mlbstatic.com/team-logos/${id}.svg`
}

function getCheck() {
    return (
        <div className="match-result flex flex-justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" fill="#e6f7e9" />
                <path d="M9 12.5l2 2 4-4.5" stroke="#2ecc71" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
        </div>
    )
}

function getCross() {
    return (
        <div className="match-result flex flex-justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                <circle cx="12" cy="12" r="10" fill="#fdedee" />
                <path d="M8 8l8 8M16 8l-8 8" stroke="#e74c3c" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
        </div>
    )
}

function renderPredictionResult(isPredictionCorrect, r, index) {
    return (
        <div className="game-result-row flex" key={index}>
            <div className="home-team flex">
                <div className="img">
                    <img src={getTeamLogoURL(r.homeTeamID)} alt="" />
                </div>
                <span className="team-name">{r.homeTeamName}</span>
                <span className="team-power">{round(r.homeTeamPower)}</span>
            </div>
            <div className="away-team flex">
                <div className="img">
                    <img src={getTeamLogoURL(r.awayTeamID)} alt="" />
                </div>
                <span className="team-name">{r.awayTeamName}</span>
                <span className="team-power">{round(r.awayTeamPower)}</span>
            </div>

            {isPredictionCorrect ? getCheck() : getCross()}
        </div>
    )
}

function DashboardAnalysisView({ data }) {
    const renderResult = function (data) {
        console.log('got data is', data)
        let { predictionCorrection, predictionInCorrection } = data
        let acc = predictionCorrection / (predictionCorrection + predictionInCorrection)
        console.log('acc is', acc)
        let accuracy = toPercentageStr(acc)
        console.log('acc is', accuracy)
        let accuracyClassName = acc && (acc * 100) >= 80 ? "good-accuracy" : "bad-accuracy"
        let spa = accuracy === '' ? '' : (<span className={accuracyClassName}>{accuracy}</span>)
        return (
            <div className="analysis-accuracy">
                <label htmlFor="">Accuracy of this sets of parameters:</label>
                {spa}
            </div>
        )
    }

    const renderDetail = function (data) {
        console.table('render data', data)

        const renderTheGame = function (gameResults = {}) {
            let ret = []
            for (let dayKey of Object.keys(gameResults)) {
                let r = {
                    'date': dayKey,
                    result: gameResults[dayKey]
                }
                ret.push(r)
            }

            return ret.map((rInstance, rInstanceIdx) => {
                return (
                    <div className="row flex" key={rInstanceIdx}>
                        <div className="date flex">
                            <span>{rInstance.date}</span>
                        </div>
                        <div className="result flex">
                            {rInstance.result.map((r, rIdx) => {
                                const isPredictionCorrect = r._isHomeTeamWin && r.homeTeamPower > r.awayTeamPower ||
                                    !r._isHomeTeamWin && r.awayTeamPower > r.homeTeamPower
                                return renderPredictionResult(isPredictionCorrect, r, rIdx)
                            })}
                        </div>
                    </div>
                )
            })

        }
        return (
            <div className="analysis-detail">
                {/* <div className="analysis-detail-title flex">
                    <div className="title">Date</div>
                    <div className="title">Result</div>
                </div> */}
                <div className="analysis-detail-game">
                    <div className="result flex flex-column">
                        {renderTheGame(data.allGamesResults)}
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="analysis-container">
            {renderResult(data)}
            {renderDetail(data)}
        </div>
    )
}

export default DashboardAnalysisView