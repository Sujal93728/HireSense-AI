function SkillGapCard({ skills }) {

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Missing Skills</h4>

                {skills.map(skill => (

                    <span
                        key={skill}
                        className="badge bg-danger me-2 mb-2"
                    >
                        {skill}
                    </span>

                ))}

            </div>

        </div>

    );

}

export default SkillGapCard;