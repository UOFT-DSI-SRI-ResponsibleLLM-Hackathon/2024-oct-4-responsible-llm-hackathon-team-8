const chatBox = document.getElementById('chat-box');

function renderChat() {
    chatBox.innerHTML = ''; // Clear previous content
    chatHistory.forEach(entry => {
        const userMessage = document.createElement('div');
        userMessage.classList.add('user-message');
        userMessage.innerHTML = `<strong>You:</strong> ${entry.user_input}`;
        chatBox.appendChild(userMessage);

        if (entry.type === 'query') {
            const sqlMessage = document.createElement('div');
            sqlMessage.classList.add('bot-message');
            sqlMessage.innerHTML = `<strong>Generated SQL Query:</strong><br><code>${entry.sql_query}</code>`;
            chatBox.appendChild(sqlMessage);

            if (entry.data) {
                const dataMessage = document.createElement('div');
                dataMessage.classList.add('bot-message');
                dataMessage.innerHTML = `${entry.data.map(row => `<li>${row.Product} - $${row.Price} (${row.Year})</li>`).join('')}`;
                chatBox.appendChild(dataMessage);
            }
        } else if (entry.type === 'message') {
            const errorMessage = document.createElement('div');
            errorMessage.classList.add('bot-message', 'text-danger');
            errorMessage.innerHTML = `${entry.data}`;
            chatBox.appendChild(errorMessage);
        }
    });
}

// Call renderChat to display chat history when the page loads
renderChat();
