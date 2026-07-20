export default function SearchBar({
  search,
  setSearch,
  location,
  setLocation,
  workType,
  setWorkType,
}) {
  return (
    <div className="grid md:grid-cols-3 gap-4 mb-6">

      <input
        type="text"
        placeholder="🔍 Search by title"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="p-3 border rounded-lg"
      />

      <input
        type="text"
        placeholder="📍 Location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        className="p-3 border rounded-lg"
      />

      <select
        value={workType}
        onChange={(e) => setWorkType(e.target.value)}
        className="p-3 border rounded-lg"
      >
        <option value="">All Work Types</option>
        <option>Full-time</option>
        <option>Part-time</option>
        <option>Contract</option>
        <option>Internship</option>
        <option>Remote</option>
      </select>

    </div>
  );
}