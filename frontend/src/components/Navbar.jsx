import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-700 text-white p-5 shadow-lg flex justify-between items-center">

      <Link to="/">
        <h1 className="text-3xl font-bold">
          HireSense AI
        </h1>
      </Link>

      <Link
        to="/resume"
        className="bg-white text-blue-700 px-4 py-2 rounded-lg font-semibold"
      >
        Resume Matcher
      </Link>

    </nav>
  );
}