import {ENDPOINTS} from "../../auth/js/config.js";

export async function userInfo() {
    console.log('userInfo выполняется')

    const response = await fetch(ENDPOINTS.user_profile, {
            method: 'GET',
            credentials: 'include', // **Отправлять cookie**
        });

    const data = await response.json();
    console.log(data);

    document.getElementById('userName').textContent = data.username || "Не указано"; // Защита от null/undefined
    document.getElementById('userEmail').textContent = data.email || "Не указано"; // Защита от null/undefined

}