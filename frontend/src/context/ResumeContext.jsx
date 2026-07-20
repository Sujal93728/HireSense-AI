import { createContext, useState } from "react";

export const ResumeContext = createContext();

export function ResumeProvider({ children }) {
  const [matches, setMatches] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [recommendedJobs, setRecommendedJobs] = useState([]);

  return (
    <ResumeContext.Provider
      value={{
        matches,
        setMatches,
        analysis,
        setAnalysis,
        recommendedJobs,
        setRecommendedJobs,
      }}
    >
      {children}
    </ResumeContext.Provider>
  );
}