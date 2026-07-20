function AIRecommendations({ recommendations }) {

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>AI Recommendations</h4>

                <ul>

                    {recommendations.map((item, index) => (

                        <li key={index}>
                            {item}
                        </li>

                    ))}

                </ul>

            </div>

        </div>

    );

}

export default AIRecommendations;