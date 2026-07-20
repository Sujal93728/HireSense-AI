import { useState } from "react";
import axios from "axios";

export default function CareerAssistant() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  async function askAI() {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      const res = await axios.post(
        "http://127.0.0.1:8000/career-assistant/ask",
        {
          question: question,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setAnswer(res.data.answer);
    } catch (err) {
      console.error(err);
      setAnswer("Unable to get AI response.");
    }

    setLoading(false);
  }

  return (
    <div className="container mt-4">

      <h2>AI Career Assistant</h2>

      <textarea
        className="form-control mt-3"
        rows="5"
        placeholder="Ask anything about your career..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button
        className="btn btn-primary mt-3"
        onClick={askAI}
      >
        {loading ? "Thinking..." : "Ask AI"}
      </button>

      {answer && (
        <div className="card mt-4">
          <div className="card-body">
            <h4>AI Response</h4>
            <p>{answer}</p>
          </div>
        </div>
      )}
    </div>
  );
}