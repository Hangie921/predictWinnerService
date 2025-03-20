import Card from "./Card";

function DashboardCardView({ cards }) {
    const getCardRows = function () {
        let tmp = Array.from(cards)
        let ret = []
        while (tmp.length) ret.push(tmp.splice(0, 3))
        return ret
    }

    return (
        <div className="cards-container">
            {
                getCardRows().map((row, rIdx) => {
                    const rowClassName = `card-row ${row.length < 3 ? 'card-row-partial' : ''}`
                    return (
                        <div className={rowClassName} key={rIdx}>
                            {row.map((card, cIdx) => (
                                <div className="card-wrapper" key={cIdx}>
                                    <Card 
                                        index={cIdx + 1}
                                        data={card}
                                    />
                                </div>
                            ))}
                        </div>
                    )
                })
            }
        </div>
    )
}

export default DashboardCardView