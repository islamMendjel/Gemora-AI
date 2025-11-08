export default function Navbar() {
  const username = localStorage.getItem("username");

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">🧠 CChatbot</h1>
      {username && <span className="text-sm">Welcome, {username}</span>}
    </nav>
  );
}
