// static/script.js
async function sendMessage() {
    const input = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    const userMessage = input.value.trim();
    if (!userMessage) return;

    chatBox.innerHTML += `<div class="user"><strong>You:</strong> ${userMessage}</div>`;
    input.value = "";
    chatBox.scrollTop = chatBox.scrollHeight;

    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await res.json();
    const botReply = data.reply || data.error || "Bot failed to respond.";

    chatBox.innerHTML += `<div class="bot"><strong>FreshBot:</strong> ${botReply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function endChat() {
    const chatBox = document.getElementById("chat-box");

    const res = await fetch("/end-chat", { method: "POST" });
    const data = await res.json();

    chatBox.innerHTML += `<div class="bot"><em>Chat ended. Summary sent and stored.</em></div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
}
