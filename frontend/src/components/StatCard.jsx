import React from "react";

function StatCard({ title, value, icon, color }) {
    return (
        <div
            className="card shadow-sm border-0"
            style={{
                borderLeft: `5px solid ${color}`,
                borderRadius: "12px"
            }}
        >
            <div className="card-body">

                <div className="d-flex justify-content-between align-items-center">

                    <div>
                        <h6 className="text-muted">{title}</h6>

                        <h2 className="fw-bold mt-2">
                            {value}
                        </h2>
                    </div>

                    <div
                        style={{
                            fontSize: 35,
                            color: color
                        }}
                    >
                        {icon}
                    </div>

                </div>

            </div>
        </div>
    );
}

export default StatCard;