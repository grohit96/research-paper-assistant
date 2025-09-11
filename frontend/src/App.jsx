import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a PDF first");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/upload_pdf", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("Upload response:", data);
      alert(`PDF uploaded successfully. ${data.chunks_indexed} chunks indexed.`);
    } catch (err) {
      console.error("Upload error:", err);
      alert("Upload failed. Check backend logs.");
    }
  };

  const handleAsk = async () => {
    if (!question) return alert("Please enter a question");
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();
      console.log("Ask response:", data);

      // Defensive checks
      setAnswer(data?.answer || "No answer received.");
      setSources(Array.isArray(data?.contexts) ? data.contexts : []);
    } catch (err) {
      console.error("Ask error:", err);
      setAnswer("Error: Could not fetch answer. Check console.");
      setSources([]);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center justify-center p-6">
      <h1 className="text-2xl font-bold mb-4 flex items-center">
        📑 Research Paper Assistant
      </h1>

      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
        className="mb-4"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 rounded mb-6"
      >
        Upload PDF
      </button>

      <input
        type="text"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="border px-3 py-2 rounded w-80 mb-4"
      />
      <button
        onClick={handleAsk}
        className="bg-green-600 text-white px-4 py-2 rounded"
      >
        Ask
      </button>

      {loading && <p className="mt-4 text-gray-600">Loading...</p>}

      {answer && !loading && (
        <div className="mt-6 p-4 bg-white shadow rounded w-full max-w-2xl">
          <h2 className="font-bold">Answer:</h2>
          <p>{String(answer)}</p>

          {sources.length > 0 && (
            <details className="mt-4">
              <summary className="cursor-pointer font-semibold">
                Sources
              </summary>
              <ul className="list-disc pl-5">
                {sources.map((s, idx) => (
                  <li key={idx} className="text-sm text-gray-600">
                    {typeof s.text === "string"
                      ? s.text
                      : JSON.stringify(s)}
                  </li>
                ))}
              </ul>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
