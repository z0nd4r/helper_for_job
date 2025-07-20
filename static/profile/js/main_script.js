import {userInfo} from "./my_profile.js";
import {copyText} from "../../helpers/js/copy_text.js";

document.addEventListener('DOMContentLoaded', async () => {
    try {
        await userInfo(); // Запускаем userInfo!

        // Добавляем обработчики событий для копирования
        const userNameSpan = document.getElementById('userName');
        const userEmailSpan = document.getElementById('userEmail');

        userNameSpan.addEventListener('click', copyText);
        userEmailSpan.addEventListener('click', copyText);

    } catch (error) {
        console.error("Error fetching user info on main page:", error);
        document.getElementById('userName').textContent = "Ошибка загрузки";
        document.getElementById('userEmail').textContent = "Ошибка загрузки";
    }
});