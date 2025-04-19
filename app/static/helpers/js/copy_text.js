// для копирования текста в профиле

export async function copyText(event) {
    const text = event.target.textContent;
    const notification = document.getElementById('copyNotification');

    try {
        await navigator.clipboard.writeText(text);

        // Show the notification
        notification.classList.add('show');

        // Hide the notification after a delay
        setTimeout(() => {
            notification.classList.remove('show');
        }, 2000); // Adjust time as needed (2 seconds in this case)

    } catch (err) {
        console.error('Не удалось скопировать текст: ', err);
        notification.textContent = "Не удалось скопировать"; // Optionally, update the notification text
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 2000);
    }
}