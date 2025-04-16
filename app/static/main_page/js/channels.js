export function initializeChannels() {

    const channelLinks = document.querySelectorAll('.channel-list a');
    const chatPlaceholder = document.getElementById('chatPlaceholder');
    const chatContainer = document.getElementById('chatContainer');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chatMessages');

    let currentChannel = null;
    let isChatActive = false;

    console.log('channelLinks:', channelLinks);
    console.log('chatPlaceholder:', chatPlaceholder);
    console.log('chatContainer:', chatContainer);
    console.log('sendButton:', sendButton);
    console.log('chatMessages:', chatMessages);

    channelLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();

            const channel = link.dataset.channel;

            if (channel !== currentChannel) {
                chatPlaceholder.style.display = 'none';
                chatContainer.style.display = 'flex';
                isChatActive = true; // **Чат теперь активен**

                if (chatMessages) {
                    chatMessages.innerHTML = '';
                }

                currentChannel = channel;
                console.log(`Выбран канал: ${channel}`);
            }
        });
    });

    if (sendButton) {
        sendButton.addEventListener('click', () => {
            if (isChatActive) {
                const messageText = messageInput.value;
                if (messageText.trim() !== '') {
                    addMessage(messageText);
                    messageInput.value = '';
                }
            } else {
                console.log('Чат не активен.  Выберите канал.');
            }
        });
    } else {
        console.error('Элемент с id="sendButton" не найден!');
    }

    if (messageInput) {
        messageInput.addEventListener('keypress', (event) => {
            if (event.key === 'Enter') {
                if (isChatActive && sendButton) {
                    sendButton.click();
                } else {
                    console.log('Чат не активен.  Выберите канал.');
                }
            }
        });
    } else {
        console.error('Элемент с id="messageInput" не найден!');
    }

    function addMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        messageElement.textContent = message;
        if (chatMessages) {
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    }
}