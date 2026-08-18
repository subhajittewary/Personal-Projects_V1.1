import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { API_VERSION } from "@second-brain/shared";

function App() {
  return <main><h1>Second Brain</h1><p>Platform foundation ready for API {API_VERSION}.</p></main>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
