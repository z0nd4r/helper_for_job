import {deleteCookie, getCookie} from "./cookie.js";
import {ENDPOINTS} from "./config.js";

// Функция для обновления access token с использованием refresh token
export async function refreshToken() {
    const refreshToken = getCookie('refreshToken');

    if (!refreshToken) {
        console.warn("Refresh token отсутствует.");
        //  Перенаправляем на страницу входа, если нет refresh token
        window.location.href = '../templates/auth.html';
        return false; //  Возвращаем false, чтобы указать, что обновление не удалось
    }

    try {
        const response = await fetch(ENDPOINTS.refreshToken, { //  Замените на ваш эндпоинт
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            const newAccessToken = data.access_token;
            setCookie('accessToken', newAccessToken, 30 * 60); // Сохраняем новый access token

            console.log("Access token успешно обновлен.");
            return true; //  Возвращаем true, чтобы указать, что обновление прошло успешно
        } else {
            console.error("Ошибка при обновлении access token:", response.status);
            //  Удаляем токены и перенаправляем на страницу входа
            await deleteCookie('accessToken');
            await deleteCookie('refreshToken');
            window.location.href = '../templates/auth.html';
            return false; //  Возвращаем false, чтобы указать, что обновление не удалось
        }
    } catch (error) {
        console.error("Ошибка при выполнении запроса обновления токена:", error);
        return false; // Возвращаем false, чтобы указать, что обновление не удалось
    }
}

//  Функция для автоматического обновления токенов
export async function autoRefreshToken() {
    //  console.log('autoRefreshToken triggered');
    try {
        const response = await fetch(ENDPOINTS.refreshToken, { //  Замените на ваш эндпоинт обновления токена
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                //  Refresh Token передается в куки - не нужно его отправлять в заголовке
            },
            credentials: 'include'
        });

        if (!response.ok) {
            //  Ошибка при обновлении токена (например, refresh token истек)
            const errorData = await response.json();
            console.error('Token refresh failed:', errorData.message || `Refresh failed: ${response.status}`);
            // Удаляем все токены и перенаправляем на страницу входа
            await deleteCookie('access_token'); // Удаляем Access Token
            await deleteCookie('refresh_token'); // Удаляем Refresh Token
            window.location.href = '../templates/auth.html'; // Перенаправляем
            return; // Прерываем выполнение, чтобы не повторять запросы
        }

        //  Если обновление токенов прошло успешно, бэк должен был установить новые куки
        //  console.log('Token refreshed successfully (backend set cookies)');

    } catch (error) {
        //  Обработка ошибок сети и т.д.
        console.error('Token refresh error:', error);
        await deleteCookie('access_token');
        await deleteCookie('refresh_token');
        window.location.href = '../templates/auth.html';
    }
}


let refreshTokenIntervalID = null
export function startTokenRefreshInterval() {
    console.log('startTokenRefreshInterval, вызов таймера для автом. обновления токенов');
    refreshTokenIntervalID = setInterval(async () => {
        await autoRefreshToken();
    },  20 * 1000); // Обновляем каждые 14 минут 59 секунд
}

export function stopTokenRefreshInterval() {
    if (refreshTokenIntervalID) {
        clearInterval(refreshTokenIntervalID);
        refreshTokenIntervalID = null;
        console.log('Автом. обновление токенов остановлено')
    }
}