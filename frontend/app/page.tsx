"use client";

import { useState } from "react";

type ChatMsg = {
  role: "user" | "ai";
  text: string;
  confidence?: number;
  escalated?: boolean;
};

export default function Home() {
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  async function sendMessage() {
    if (!input.trim() || loading) return;

    const userMsg: ChatMsg = { role: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/chat/simple`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMsg.text }),
      });

      const data = await res.json();

      const aiMsg: ChatMsg = {
        role: "ai",
        text: data.reply,
        confidence: data.confidence,
        escalated: data.escalated,
      };

      setMessages(prev => [...prev, aiMsg]);
    } catch {
      setMessages(prev => [
        ...prev,
        { role: "ai", text: "Backend error" },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ maxWidth: 650, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>AI Support Chat</h1>

      <div style={{ border: "1px solid #ccc", padding: 16, minHeight: 320 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: 12 }}>
            <div style={{ textAlign: m.role === "user" ? "right" : "left" }}>
              <b>{m.role === "user" ? "You" : "AI"}:</b> {m.text}
            </div>

            {m.role === "ai" && (
              <div style={{ fontSize: 12, color: "#555", marginTop: 4 }}>
                {m.confidence !== undefined && (
                  <span>Confidence: {(m.confidence * 100).toFixed(0)}%</span>
                )}
                {m.escalated && (
                  <span style={{ color: "red", marginLeft: 10 }}>
                    Escalated to Human
                  </span>
                )}
              </div>
            )}
          </div>
        ))}

        {loading && <p>AI typing...</p>}
      </div>

      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === "Enter" && sendMessage()}
        placeholder="Type your message..."
        style={{ width: "100%", padding: 10, marginTop: 10 }}
      />
    </main>
  );
}
