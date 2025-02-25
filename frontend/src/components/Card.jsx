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

const fakeMatches = {
    matchID: 745707,
    name: {
        home: "Yankees",
        away: "Guardians"
    },
    powerRanking: {
        home: 1.5110000000000001,
        away: 1.233
    },
    starter: {
        home: {
            name: "Luis Gil",
            handed: "RHP",
            record: "12-6",
            so: 144,
        },
        away: {
            name: "Matthew Boyd",
            handed: "LHP",
            record: "0-0",
            so: 8,
        }
    },
    overall: {
        home: {
            record: "73-53",
            percentage: ".579"
        },
        away: {
            record: "73-52",
            percentage: ".584"
        }
    },
    homeAway: {
        home: {
            record: "32-28",
            percentage: ".533"
        },
        away: {
            record: "35-32",
            percentage: ".522"
        }
    },
    handed: {
        home: {
            record: "13-20",
            percentage: ".394"
        },
        away: {
            record: "47-43",
            percentage: ".522"
        }
    },
    l10: {
        home: {
            record: "5-5",
            percentage: ".500"
        },
        away: {
            record: "6-4",
            percentage: ".600"
        }
    },
    streak: {
        home: {
            isWin: false,
            streak: 3
        },
        away: {
            isWin: true,
            streak: 1
        }
    },
    diff: {
        home: 112,
        away: 82
    },
    winner: {
        home: false,
        away: true
    }
}

function Card(props) {
    console.log('fake is', fakeMatches)
    function round(from) {
        return Math.round(from * 1000) / 1000
    }
    return (
        <div className="card">
            <div className="card__team flex flex-justify-between">
                <span className="team__home ">{fakeMatches.name.home + props.index}</span>
                <span className="team__away">{fakeMatches.name.away}</span>
            </div>
            <div className="card__power flex flex-justify-between">
                <span className="power_home">{round(fakeMatches.powerRanking.home)}</span>
                <span className="power_away">{round(fakeMatches.powerRanking.away)}</span>
            </div>
            <div className="card__starter">
                <div className="">
                    <span>Starter</span>
                </div>
            </div>
            <div className="card__starter flex flex-justify-between">
                <div className="starter__label">
                    <span>Home</span>
                </div>
                <div className="starter__value">
                    <span>{fakeMatches.starter.home.name}</span>
                </div>
                <div className="starter__value flex flex-justify-between">
                    <span>{fakeMatches.starter.home.handed} </span>
                    <span>{fakeMatches.starter.home.record}</span>
                    <span>{fakeMatches.starter.home.so} SO</span>
                </div>
            </div>
            <div className="card__starter flex flex-justify-between">
                <div className="starter__label">
                    <span>Away</span>
                </div>
                <div className="starter__value">
                    <span>{fakeMatches.starter.away.name}</span>
                </div>
                <div className="starter__value flex flex-justify-between">
                    <span>{fakeMatches.starter.away.handed}</span>
                    <span>{fakeMatches.starter.away.record}</span>
                    <span>{fakeMatches.starter.away.so} SO</span>
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
            <div className="card__overall">
                <div className="overall flex">
                    <div className="card__label">
                        <span>Overall</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.overall.home.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.overall.home.percentage}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.overall.away.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.overall.away.percentage}</span>
                    </div>
                </div>
            </div>
            <div className="card__home__away">
                <div className="home_away flex">
                    <div className="card__label">
                        <span>Home/Away</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.homeAway.home.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.homeAway.home.percentage}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.homeAway.away.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.homeAway.away.percentage}</span>
                    </div>
                </div>
            </div>
            <div className="card__handed">
                <div className="handed flex">
                    <div className="card__label">
                        <span>Handed</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.handed.home.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.handed.home.percentage}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.handed.away.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.handed.away.percentage}</span>
                    </div>
                </div>
            </div>
            <div className="card__l10">
                <div className="l10 flex">
                    <div className="card__label">
                        <span>l10</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.l10.home.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.l10.home.percentage}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.l10.away.record}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.l10.away.percentage}</span>
                    </div>
                </div>
            </div>
            <div className="card__streak">
                <div className="streak flex">
                    <div className="card__label">
                        <span>Streak</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.streak.home.isWin ? "W" : "L"}{fakeMatches.streak.home.streak}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.streak.away.isWin ? "W" : "L"}{fakeMatches.streak.away.streak}</span>
                    </div>
                </div>
            </div>
            <div className="card__diff">
                <div className="diff flex">
                    <div className="card__label">
                        <span>Diff</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.diff.home}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.diff.away}</span>
                    </div>
                </div>
            </div>
            <div className="card__winner">
                <div className="winner flex">
                    <div className="card__label">
                        <span>Winner</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.winner.home ? "True" : "False"}</span>
                    </div>
                    <div className="card__value">
                        <span>{fakeMatches.winner.away ? "True" : "False"}</span>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Card