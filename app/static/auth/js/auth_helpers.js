import {getCookie} from "./cookie.js";
import {refreshToken} from "./tokens.js";

// Функция, которая будет выполнена при загрузке страницы
export async function initializeAuthentication() {
    if (getCookie('refresh_token')) {
        console.log("Refresh token найден. Попытка обновления access token...");
        const refreshSuccessful = await refreshToken(); //  Обновляем access token

        if (refreshSuccessful) {
            //  Если обновление прошло успешно, можно продолжать работу с сайтом
            console.log("Пользователь аутентифицирован.");
            //  Выполните действия, необходимые для аутентифицированного пользователя
        } else {
            //  Если обновление не удалось, перенаправляем на страницу входа
            console.log("Не удалось обновить access token. Перенаправляем на страницу входа.");
        }
    } else {
        //  Если refresh token отсутствует, перенаправляем на страницу входа
        console.log("Refresh token не найден. Перенаправляем на страницу входа.");
        // window.location.href = '../templates/auth.html';
    }
}
