import "../styles/Card.scss"


// Card is the main component displays the match of
// 2 teams with the team stats and the power ranking

// No.15
// +++++++++++++++++++++++++++++++++++++++++++++++++
// Match ID: 745707
// Home: (147) Yankees   1.5110000000000001
// Away: (114) Guardians  1.233
// +++++++++++++++++++++++++++++++++++++++++++++++++
// Home Starter: Luis Gil (661563)           RHP 12-6 3.39 144SO
// Away Starter: Matthew Boyd (571510)       LHP 0-0 3.38 8SO

// Item             Home Team       Away Team       Compare
// Overall          73-53   .579    73-52   .584    away team
// Home/Away        32-28   .533    35-32   .522    home team
// Handed           13-20   .394    47-43   .522    away team
// l10              5-5     .500    6-4     .600
// Streak           L3              W1
// Diff             112             82
// Winner           False           True


const GAME_GAME_ID_JSON_KEY = "gameID"
const GAME_GAME_DATE_JSON_KEY = "gameDate"
const GAME_HOME_TEAM_JSON_KEY = "homeTeam"
const GAME_AWAY_TEAM_JSON_KEY = "awayTeam"
const GAME_NAME_JSON_KEY = "name"
const GAME_OVERALL_WINS_JSON_KEY = "overallWins"
const GAME_OVERALL_LOSS_JSON_KEY = "overallLosses"
const GAME_HOME_WINS_JSON_KEY = "homeWins"
const GAME_HOME_LOSS_JSON_KEY = "homeLosses"
const GAME_AWAY_WINS_JSON_KEY = "awayWins"
const GAME_AWAY_LOSS_JSON_KEY = "awayLosses"
const GAME_LEFT_HANDED_WINS_JSON_KEY = "lHandedWins"
const GAME_LEFT_HANDED_LOSS_JSON_KEY = "lHandedLosses"
const GAME_RIGHT_HANDED_WINS_JSON_KEY = "rHandedWins"
const GAME_RIGHT_HANDED_LOSS_JSON_KEY = "rHandedLosses"
const GAME_LAST_10_WINS_JSON_KEY = "l10Wins"
const GAME_LAST_10_LOSS_JSON_KEY = "l10Losses"
const GAME_DIFF_JSON_KEY = "diff"
const GAME_STREAK_IS_WIN_JSON_KEY = "streakIsWin"
const GAME_STREAK_JSON_KEY = "streak"
const GAME_PITCHER_JSON_KEY = "pitcher"
const GAME_PITCHER_ERA_JSON_KEY = "era"
const GAME_PITCHER_WINS_JSON_KEY = "wins"
const GAME_PITCHER_LOSS_JSON_KEY = "losses"

const GAME_JSON = {
    [GAME_GAME_ID_JSON_KEY]: 746196,
    [GAME_GAME_DATE_JSON_KEY]: "2024-08-01",
    [GAME_HOME_TEAM_JSON_KEY]: {
        [GAME_NAME_JSON_KEY]: "Angels",
        [GAME_OVERALL_WINS_JSON_KEY]: 47,
        [GAME_OVERALL_LOSS_JSON_KEY]: 62,
        [GAME_HOME_WINS_JSON_KEY]: 24,
        [GAME_HOME_LOSS_JSON_KEY]: 34,
        [GAME_AWAY_WINS_JSON_KEY]: 23,
        [GAME_AWAY_LOSS_JSON_KEY]: 28,
        [GAME_LEFT_HANDED_WINS_JSON_KEY]: 8,
        [GAME_LEFT_HANDED_LOSS_JSON_KEY]: 11,
        [GAME_RIGHT_HANDED_WINS_JSON_KEY]: 8,
        [GAME_RIGHT_HANDED_LOSS_JSON_KEY]: 11,
        [GAME_LAST_10_WINS_JSON_KEY]: 5,
        [GAME_LAST_10_LOSS_JSON_KEY]: 5,
        [GAME_DIFF_JSON_KEY]: -94,
        [GAME_STREAK_IS_WIN_JSON_KEY]: false,
        [GAME_STREAK_JSON_KEY]: 2,
        [GAME_PITCHER_JSON_KEY]: {
            [GAME_NAME_JSON_KEY]: "Carson Fulmer",
            [GAME_PITCHER_ERA_JSON_KEY]: 3.69,
            [GAME_PITCHER_WINS_JSON_KEY]: 0,
            [GAME_PITCHER_LOSS_JSON_KEY]: 2
        }
    },
    [GAME_AWAY_TEAM_JSON_KEY]: {
        [GAME_NAME_JSON_KEY]: "Rockies",
        [GAME_OVERALL_WINS_JSON_KEY]: 40,
        [GAME_OVERALL_LOSS_JSON_KEY]: 70,
        [GAME_HOME_WINS_JSON_KEY]: 24,
        [GAME_HOME_LOSS_JSON_KEY]: 29,
        [GAME_AWAY_WINS_JSON_KEY]: 16,
        [GAME_AWAY_LOSS_JSON_KEY]: 41,
        [GAME_LEFT_HANDED_WINS_JSON_KEY]: 12,
        [GAME_LEFT_HANDED_LOSS_JSON_KEY]: 21,
        [GAME_RIGHT_HANDED_WINS_JSON_KEY]: 12,
        [GAME_RIGHT_HANDED_LOSS_JSON_KEY]: 21,
        [GAME_LAST_10_WINS_JSON_KEY]: 4,
        [GAME_LAST_10_LOSS_JSON_KEY]: 6,
        [GAME_DIFF_JSON_KEY]: -174,
        [GAME_STREAK_IS_WIN_JSON_KEY]: true,
        [GAME_STREAK_JSON_KEY]: 2,
        [GAME_PITCHER_JSON_KEY]: {
            [GAME_NAME_JSON_KEY]: "Ryan Feltner",
            [GAME_PITCHER_ERA_JSON_KEY]: 4.97,
            [GAME_PITCHER_WINS_JSON_KEY]: 1,
            [GAME_PITCHER_LOSS_JSON_KEY]: 10
        }
    }
}

const winningOptOverall = 0
const winningOptLast10 = 1
const winningOptHomeAway = 2


function Card({ data }) {
    const match = data
    if (match.gameID === 'fake') return (<div className="card no_border"></div>)

    function round(from) {
        return Math.round(from * 1000) / 1000
    }

    function calculateWinning(win, loss) {
        return round(win / loss)
    }

    function getNormalWinning(whichWeight, homeTeam, awayTeam) {
        let containerClassName = ""
        let labelName = ""
        let homeWins = 0
        let homeLosses = 0
        let awayWins = 0
        let awayLosses = 0

        switch (whichWeight) {
            case winningOptHomeAway:
                containerClassName = "card__home_away"
                labelName = "Home/Away"
                homeWins = homeTeam.homeWins
                homeLosses = homeTeam.homeLosses
                awayWins = awayTeam.awayWins
                awayLosses = awayTeam.awayLosses
                break
            case winningOptLast10:
                containerClassName = "card__l10"
                labelName = "Last 10"
                homeWins = homeTeam.l10Wins
                homeLosses = homeTeam.l10Losses
                awayWins = awayTeam.l10Wins
                awayLosses = awayTeam.l10Losses
                break
            case winningOptOverall:
                containerClassName = "card__overall"
                labelName = "Overall"
                homeWins = homeTeam.overallWins
                homeLosses = homeTeam.overallLosses
                awayWins = awayTeam.overallWins
                awayLosses = awayTeam.overallLosses
                break
            default:
                console.error('not supported')
        }
        return (
            <div className={containerClassName + " flex"}>
                <div className="card__label">
                    <span>{labelName}</span>
                </div>
                <div className="card__value">
                    <span>{homeWins}-{homeLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(homeWins / (homeWins + homeLosses))}</span>
                </div>
                <div className="card__value">
                    <span>{awayWins}-{awayLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(awayWins / (awayWins + awayLosses))}</span>
                </div>
            </div>
        )

    }

    function getLast10Winning(home, away) {
        let homeWins = home.l10Wins
        let homeLosses = home.l10Losses
        let awayWins = away.l10Wins
        let awayLosses = away.l10Losses

        return (
            <div className="card__l10 flex">
                <div className="card__label">
                    <span>Last 10</span>
                </div>
                <div className="card__value">
                    <span>{homeWins}-{homeLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(homeWins / (homeWins + homeLosses))}</span>
                </div>
                <div className="card__value">
                    <span>{awayWins}-{awayLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(awayWins / (awayWins + awayLosses))}</span>
                </div>
            </div>
        )
    }

    function getHandedWinning(home, away) {
        let homeWins = 0
        let homeLosses = 0
        let awayWins = 0
        let awayLosses = 0

        if (away.pitcher.handed === 'LHP') {
            homeWins = home.lHandedWins
            homeLosses = home.lHandedLosses
        } else {
            homeWins = home.rHandedWins
            homeLosses = home.rHandedLosses
        }
        if (home.pitcher.handed === 'LHP') {
            awayWins = away.lHandedWins
            awayLosses = away.lHandedLosses
        } else {
            awayWins = away.rHandedWins
            awayLosses = away.rHandedLosses
        }
        return (
            <div className="card__handed flex">
                <div className="card__label">
                    <span>Handed</span>
                </div>
                <div className="card__value">
                    <span>{homeWins}-{homeLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(homeWins / (homeWins + homeLosses))}</span>
                </div>
                <div className="card__value">
                    <span>{awayWins}-{awayLosses}</span>
                </div>
                <div className="card__value">
                    <span>{round(awayWins / (awayWins + awayLosses))}</span>
                </div>
            </div>
        )
    }

    function getStreakWinning(home, away) {
        return (
            <div className="card__streak flex">
                <div className="card__label">
                    <span>Streak</span>
                </div>
                <div className="card__value">
                    <span>{home.streakIsWin ? "W" : "L"}{home.streak}</span>
                </div>
                <div className="card__value">
                    <span>{away.streakIsWin ? "W" : "L"}{away.streak}</span>
                </div>
            </div>
        )
    }
    return (
        <div className="card">
            <div className="card__team flex flex-justify-between">
                <span className="team__home">{match.homeTeam.name}</span>
                <span className="team__away">{match.awayTeam.name}</span>
            </div>
            <div className="card__power flex flex-justify-between">
                <span className="power_home">{round(match.homeTeam.power)}</span>
                <span className="power_away">{round(match.awayTeam.power)}</span>
            </div>
            <div className="card__starter">
                <div className="">
                    <span>Starter</span>
                </div>
            </div>
            <div className="card__starter flex flex-wrap">
                <div className="starter__label">
                    <span>Home</span>
                </div>
                <div className="starter__value starter__name">
                    <span>{match.homeTeam.pitcher.name}</span>
                </div>
                <div className="starter__label"></div>
                <div className="starter__value flex flex-justify-between">
                    <span>{match.homeTeam.pitcher.handed} </span>
                    <span>{match.homeTeam.pitcher.wins}-{match.homeTeam.pitcher.losses} {match.homeTeam.pitcher.era}</span>
                    <span>{match.homeTeam.pitcher.so} SO</span>
                </div>
            </div>
            <div className="card__starter flex flex-wrap">
                <div className="starter__label">
                    <span>Away</span>
                </div>
                <div className="starter__value starter__name">
                    <span>{match.awayTeam.pitcher.name}</span>
                </div>
                <div className="starter__label"></div>
                <div className="starter__value flex flex-justify-between">
                    <span>{match.awayTeam.pitcher.handed}</span>
                    <span>{match.awayTeam.pitcher.wins}-{match.awayTeam.pitcher.losses} {match.awayTeam.pitcher.era}</span>
                    <span>{match.awayTeam.pitcher.so} SO</span>
                </div>
            </div>
            <div className="card__sub_title flex">
                <div className="card__label"></div>
                <div className="card__label">
                    <span>Home</span>
                </div>
                <div className="card__label">
                    <span>Away</span>
                </div>
            </div>
            {getNormalWinning(winningOptOverall, match.homeTeam, match.awayTeam)}
            {getNormalWinning(winningOptHomeAway, match.homeTeam, match.awayTeam)}
            {getHandedWinning(match.homeTeam, match.awayTeam)}
            {getNormalWinning(winningOptLast10, match.homeTeam, match.awayTeam)}
            {getStreakWinning(match.homeTeam, match.awayTeam)}
            <div className="card__diff">
                <div className="diff flex">
                    <div className="card__label">
                        <span>Diff</span>
                    </div>
                    <div className="card__value">
                        <span>{match.homeTeam.diff}</span>
                    </div>
                    <div className="card__value">
                        <span>{match.awayTeam.diff}</span>
                    </div>
                </div>
            </div>
            {/* <div className="card__winner">
                <div className="winner flex">
                    <div className="card__label">
                        <span>Winner</span>
                    </div>
                    <div className="card__value">
                        <span>{match.winner.home ? "True" : "False"}</span>
                    </div>
                    <div className="card__value">
                        <span>{match.winner.away ? "True" : "False"}</span>
                    </div>
                </div>
            </div> */}
        </div>
    )
}

export default Card