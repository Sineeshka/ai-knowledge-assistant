import { useState } from "react";

import "./App.css";

import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import UploadDocument from "./components/UploadDocument";
import QuestionBox from "./components/QuestionBox";
import AnswerCard from "./components/AnswerCard";
import SourceList from "./components/SourceList";


function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);

  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState("");


  // -------------------------
  // File selection
  // -------------------------

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
    setUploadMessage("");
  };


  // -------------------------
  // Upload document
  // -------------------------

  const uploadDocument = async () => {
    if (!file) {
      setUploadMessage(
        "Please select a PDF first."
      );

      return;
    }

    setUploading(true);
    setUploadMessage("");

    const formData = new FormData();

    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/documents/upload",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Upload failed"
        );
      }

      setUploadMessage(
        `${data.filename} uploaded successfully.`
      );

      setFile(null);

    } catch (error) {
      console.error(error);

      setUploadMessage(
        "Upload failed. Please try again."
      );
    }

    setUploading(false);
  };


  // -------------------------
  // Ask question
  // -------------------------

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/ask?q=${encodeURIComponent(
          question
        )}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Request failed"
        );
      }

      setAnswer(data.answer);
      setSources(data.sources || []);

    } catch (error) {
      console.error(error);

      setAnswer(
        "Something went wrong. Please try again."
      );
    }

    setLoading(false);
  };


  // -------------------------
  // Enter key
  // -------------------------

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      askQuestion();
    }
  };


  return (
    <div className="app">

      <Sidebar />

      <main className="main">

        <Header />

        <div className="content">

          <UploadDocument
            file={file}
            uploading={uploading}
            uploadMessage={uploadMessage}
            onFileChange={handleFileChange}
            onUpload={uploadDocument}
          />

          <QuestionBox
            question={question}
            loading={loading}
            onQuestionChange={(event) =>
              setQuestion(event.target.value)
            }
            onAsk={askQuestion}
            onKeyDown={handleKeyDown}
          />

          <AnswerCard
            answer={answer}
          />

          <SourceList
            sources={sources}
          />

        </div>

      </main>

    </div>
  );
}


export default App;