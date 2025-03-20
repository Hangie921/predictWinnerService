import Card from "./Card";

function DashboardCardView({ cards }) {
    const getCardRows = function () {
        let tmp = Array.from(cards)
        let ret = []
        while (tmp.length) ret.push(tmp.splice(0, 3))
        return ret
    }

    return (
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
    )
}

export default DashboardCardView