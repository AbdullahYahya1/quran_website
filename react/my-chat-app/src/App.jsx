import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false); // Add isLoading state

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return; // Also check if isLoading is true

    setIsLoading(true); // Set isLoading to true when the request starts
    setMessages([...messages, { sender: 'user', text: input }]);

    try {
      const response = await axios.get(`http://127.0.0.1:8000/search/?query=${encodeURIComponent(input)}`);
      const apiResponses = response.data.results;
      apiResponses.forEach(item => {
        const messageText = `${item.surah_name}:${item.text}`;
        setMessages(prevMessages => [...prevMessages, { sender: 'api', text: messageText }]);
      });
    } catch (error) {
      console.error("Error calling the API:", error);
      setMessages(prevMessages => [...prevMessages, { sender: 'api', text: "Failed to get a response." }]);
    }

    setInput('');
    setIsLoading(false); // Set isLoading to false when the request is complete
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>QU Chat</h1>
      </header>
      <div className="chat-box">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
      </div>
      <form onSubmit={sendMessage}>
        <input
          type="text"
          value={input}
          disabled={isLoading} // Optionally disable input while loading
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button type="submit" disabled={isLoading}>Send</button> {/* Disable button based on isLoading */}
      </form>
    </div>
  );
}

export default App;
