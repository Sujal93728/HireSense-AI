function ResumeScore({ score }) {

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Resume Score</h4>

                <h1>{score}%</h1>

                <p className="text-success">
                    Excellent Resume
                </p>

            </div>

        </div>

    );

}

export default ResumeScore;