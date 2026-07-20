function RecentInterviews({ interviews }) {

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Recent Interviews</h4>

                <table className="table">

                    <thead>

                        <tr>

                            <th>Role</th>

                            <th>Difficulty</th>

                            <th>Score</th>

                        </tr>

                    </thead>

                    <tbody>

                        {interviews.map(interview => (

                            <tr key={interview.id}>

                                <td>{interview.role}</td>

                                <td>{interview.difficulty}</td>

                                <td>{interview.score}</td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>

    );

}

export default RecentInterviews;