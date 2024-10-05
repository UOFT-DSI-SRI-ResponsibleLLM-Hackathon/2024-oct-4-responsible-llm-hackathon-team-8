const chatHistory = [];

// Function to set the database link
async function setDbLink(event) {
    event.preventDefault(); // Prevent form submission
    const dbLink = document.getElementById('db-link').value;

    const response = await fetch('http://localhost:5000/api/set_db_link', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ db_link: dbLink })
    });

    const result = await response.json();
    if (result.status === 'Connected') {
        alert(result.message);
    } else {
        alert(result.message);
    }
}

// Function to query the database
async function queryDatabase(event) {
    event.preventDefault(); // Prevent form submission
    const userInput = document.getElementById('user-input').value;

    const response = await fetch('http://localhost:5000/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_input: userInput })
    });

    const result = await response.json();
    if (result.sql_query) {
        chatHistory.push({
            user_input: userInput,
            sql_query: result.sql_query,
            data: result.data,
            type: 'query'
        });
        displayChatHistory();
    } else {
        chatHistory.push({
            user_input: userInput,
            data: result.message,
            type: 'message'
        });
        displayChatHistory();
    }

    document.getElementById('user-input').value = ''; // Clear input
}

// Function to display chat history
function displayChatHistory() {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = ''; // Clear chat box

    chatHistory.forEach(entry => {
        const messageDiv = document.createElement('div');
        
        // Define styles based on the message type
        if (entry.type === 'query') {
            messageDiv.className = 'bg-light p-2 my-1'; // Styling for query
            messageDiv.innerText = `You: ${entry.user_input}\nSQL Query: ${entry.sql_query}\nData: ${JSON.stringify(entry.data, null, 2)}`; 
        } else if (entry.type === 'message') {
            messageDiv.className = 'bg-warning p-2 my-1'; // Styling for system message
            messageDiv.innerText = `You: ${entry.user_input}\nSystem: ${entry.message}`;
        }

        chatBox.appendChild(messageDiv);
    });

    // Scroll to the bottom of the chat box
    chatBox.scrollTop = chatBox.scrollHeight;
}
