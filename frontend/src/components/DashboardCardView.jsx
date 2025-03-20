import Card from "./Card";

function DashboardCardView({ cards }) {
    return (
        <div className="cards-container">
            {cards.map((card, idx) => (
                <div className="card-wrapper" key={card.gameID || idx}>
                    <Card 
                        index={idx + 1}
                        data={card}
                    />
                </div>
            ))}
        </div>
    )
}

export default DashboardCardView