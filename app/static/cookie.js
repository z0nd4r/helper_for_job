import {ENDPOINTS} from "./config.js";

// Отправляет запрос на сервер для удаления cookie (HttpOnly)
export async function deleteCookie(name) {
    console.log(`[server] Попытка удаления cookie (server-side): ${name}`);
    try {
        const response = await fetch(ENDPOINTS.delete_cookie, { //  Укажите правильный URL
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ cookie_name: name }) //  Передаем имя cookie в теле запроса
        });

        if (response.ok) {
            const data = await response.json();
            console.log(`[server] Cookie (server-side) удален: ${data.message}`);
        } else {
            console.error(`[server] Ошибка при удалении cookie (server-side): ${response.status}`);
        }
    } catch (error) {
        console.error(`[server] Ошибка при отправке запроса на удаление cookie:`, error);
    }
}

export function getCookie(name) {
    const cookieName = name + "=";
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(cookieName) === 0) {
            return c.substring(cookieName.length, cookieName.length + c.substring(cookieName.length).indexOf(';')); // Изменено
        }
    }
    return "";
}