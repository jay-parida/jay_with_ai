"use client";
import { useState, useEffect, useRef } from "react";

export default function ChatBot() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const chatEndRef = useRef(null);

  const sendMessage = async () => {
    if (!input) return;

    const userMessage = { role: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: input }),
      });

      const data = await res.json();

      const botMessage = {
        role: "bot",
        text: data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Server error 😢" },
      ]);
    }

    setInput("");
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div style={styles.wrapper}>
      
      {/* LEFT SIDE (HERO) */}
      <div style={styles.left}>
        <p style={styles.small}>Hello 👋</p>

        <h1 style={styles.title}>
          HireMe <span style={styles.highlight}>AI</span>
        </h1>

        <h2 style={styles.subtitle}>
          Your Intelligent HR & Career Assistant
        </h2>

        <p style={styles.desc}>
          Ask anything about jobs, resumes, interview prep, and career growth.
          This AI will guide you like a real HR.
        </p>
      </div>

      {/* RIGHT SIDE (CHATBOT) */}
      <div style={styles.right}>
        <div style={styles.chatContainer}>
          
          <div style={styles.chatBox}>
            {messages.map((msg, i) => (
              <div
                key={i}
                style={{
                  ...styles.message,
                  alignSelf:
                    msg.role === "user" ? "flex-end" : "flex-start",
                  background:
                    msg.role === "user"
                      ? "#7c3aed"
                      : "rgba(255,255,255,0.1)",
                  color: "white",
                }}
              >
                {msg.text}
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>

          <div style={styles.inputArea}>
            <input
              style={styles.input}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask something..."
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            />
            <button style={styles.button} onClick={sendMessage}>
              ➤
            </button>
          </div>

        </div>
      </div>
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    height: "100vh",
    background: "radial-gradient(circle at top, #1a0033, #050010)",
    color: "white",
    padding: "40px",
    gap: "40px",
  },

  left: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
  },

  small: {
    color: "#a78bfa",
    marginBottom: "10px",
  },

  title: {
    fontSize: "60px",
    fontWeight: "bold",
  },

  highlight: {
    color: "#a855f7",
  },

  subtitle: {
    fontSize: "24px",
    marginTop: "10px",
    color: "#c4b5fd",
  },

  desc: {
    marginTop: "20px",
    maxWidth: "500px",
    color: "#d1d5db",
    lineHeight: "1.6",
  },

  right: {
    flex: 1,
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
  },

  chatContainer: {
    width: "100%",
    maxWidth: "400px",
    height: "70vh",
    backdropFilter: "blur(20px)",
    background: "rgba(255,255,255,0.05)",
    borderRadius: "20px",
    display: "flex",
    flexDirection: "column",
    overflow: "hidden",
    border: "1px solid rgba(255,255,255,0.1)",
  },

  chatBox: {
    flex: 1,
    padding: "15px",
    display: "flex",
    flexDirection: "column",
    gap: "10px",
    overflowY: "auto",
  },

  message: {
    padding: "10px 14px",
    borderRadius: "12px",
    maxWidth: "75%",
    fontSize: "14px",
  },

  inputArea: {
    display: "flex",
    borderTop: "1px solid rgba(255,255,255,0.1)",
  },

  input: {
    flex: 1,
    padding: "12px",
    background: "transparent",
    border: "none",
    outline: "none",
    color: "white",
  },

  button: {
    padding: "12px 16px",
    background: "#7c3aed",
    border: "none",
    color: "white",
    cursor: "pointer",
  },
};