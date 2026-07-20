export const startInterview = (role, difficulty) =>
  api.post("/interview/start", {
    role,
    difficulty,
  });

export const submitAnswer = (data) =>
  api.post("/interview/answer", data);

function Interview() {
    return (
        <div>
            Interview Page
        </div>
    )
}

export default Interview;
