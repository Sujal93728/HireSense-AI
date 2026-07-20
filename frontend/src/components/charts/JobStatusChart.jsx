import {
    BarChart,
    Bar,
    Tooltip,
    XAxis,
    YAxis,
    ResponsiveContainer
} from "recharts";

function JobStatusChart({ data }) {

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Applications</h4>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <BarChart data={data}>

                        <XAxis dataKey="status" />

                        <YAxis />

                        <Tooltip />

                        <Bar
                            dataKey="count"
                            fill="#2563eb"
                        />

                    </BarChart>

                </ResponsiveContainer>

            </div>

        </div>

    );

}

export default JobStatusChart;