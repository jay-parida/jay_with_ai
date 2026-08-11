"use client";

import ChatBot from "./components/ChatBot";

export default function Home() {
  return (
    <main style={{ padding: "20px", textAlign: "center" }}>
      <h1>HireMe AI 🤖</h1>
      <ChatBot />
    </main>
  );
}