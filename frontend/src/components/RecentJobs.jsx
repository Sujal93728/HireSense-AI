function RecentJobs({ jobs = [] }) {
    return (
        <div className="card shadow-sm">
            <div className="card-body">
                <h4>Recommended Jobs</h4>

                {jobs.length === 0 ? (
                    <p>No recommended jobs yet.</p>
                ) : (
                    <ul className="list-group">
                        {jobs.map((job) => (
                            <li
                                key={job.job_id}
                                className="list-group-item"
                            >
                                <strong>{job.title}</strong>
                                <br />
                                {job.company_name}
                            </li>
                        ))}
                    </ul>
                )}
            </div>
        </div>
    );
}

export default RecentJobs;