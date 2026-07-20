import {
    PieChart,
    Pie,
    Tooltip,
    Cell,
    ResponsiveContainer
} from "recharts";

const COLORS = [
    "#2563eb",
    "#16a34a",
    "#f59e0b",
    "#dc2626",
    "#9333ea"
];

function SkillDistribution({ data }) {

    return (
        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Skill Distribution</h4>

                <ResponsiveContainer
                    width="100%"
                    height={300}
                >

                    <PieChart>

                        <Pie
                            data={data}
                            dataKey="value"
                            nameKey="name"
                            outerRadius={100}
                        >

                            {data.map((entry, index) => (
                                <Cell
                                    key={index}
                                    fill={
                                        COLORS[
                                            index % COLORS.length
                                        ]
                                    }
                                />
                            ))}

                        </Pie>

                        <Tooltip />

                    </PieChart>

                </ResponsiveContainer>

            </div>

        </div>
    );

}

export default SkillDistribution;