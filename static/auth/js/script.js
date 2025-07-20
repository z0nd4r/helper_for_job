import {login, register} from './auth.js'
import {deleteCookie, getCookie} from "./cookie.js";
import {startTokenRefreshInterval, stopTokenRefreshInterval} from "./tokens.js";
import {initializeAuthentication} from "./auth_helpers.js";
import {userInfo} from "../../profile/js/my_profile.js";

// document.addEventListener('DOMContentLoaded', initializeAuthentication);

document.addEventListener('DOMContentLoaded', () => {
    const authViewContainer = document.getElementById('auth-view-container');
    const loginButton = document.getElementById('login-button');
    const registerLink = document.getElementById('register-link');
    const loginLink = document.getElementById('login-link');
    const registerButton = document.getElementById('register-button');
    const loginForm = document.getElementById('auth-view-login'); // Получите форму логина
    const logoutButton = document.getElementById('logout-button');

    // Вызываем функцию initializeAuthentication() при загрузке страницы



    // // Функция для отправки запросов к API с автоматическим обновлением токена
    // async function apiRequest(url, options) {
    //     //  console.log('apiRequest called for', url);
    //     //  Здесь не нужно читать access_token из куки, если бэк установил куки HttpOnly и access token
    //     const accessToken = null; // Устанавливаем null, так как JS не имеет доступа к HttpOnly куки
    //     const headers = {
    //         ...options.headers,
    //         //  'Authorization': `Bearer ${accessToken}`, //  Access Token передаем в заголовке (если нужно), если доступа нет, вызовем refresh token
    //     };
    //
    //     try {
    //         //  Если нет access token  (или access token, если мы получим его от  getCookie), то обновляем
    //         //  If your backend is using HTTP-only cookies then this step is not necessary.
    //         if (!accessToken) {
    //             //  console.log('No access token. Refreshing...');
    //             await autoRefreshToken(); // Обновляем токены
    //         }
    //
    //         //  После обновления (или если access token был), можем сделать запрос.  Важно, чтобы на данном этапе
    //         //  был access token.
    //         //  const newAccessToken = getCookie('accessToken');  // Если JS имел бы доступ к токену, то получаем его
    //         const newAccessToken = null; //  Устанавливаем null, так как не можем получить доступ
    //         if (newAccessToken) {
    //             //console.log("Access token after refresh: ", newAccessToken);
    //             headers['Authorization'] = `Bearer ${newAccessToken}`; //  Добавляем Authorization, если получили токен
    //         }
    //         const newOptions = {
    //             ...options,
    //             headers: headers
    //         };
    //
    //         const response = await fetch(url, newOptions);
    //
    //         //  Обработка 401 (Unauthorized) - токен, вероятно, истек
    //         if (response.status === 401) {
    //             //  console.log('API request 401 Unauthorized. Refreshing...');
    //             await autoRefreshToken(); //  Попытка обновить токены еще раз
    //
    //             //  Повторяем запрос
    //             // const refreshedAccessToken = getCookie('accessToken'); //  Попытка прочитать access_token
    //             const refreshedAccessToken = null; //  Поскольку токен в куки, то его просто нет
    //             if (refreshedAccessToken) {
    //                 //console.log("Access token after refresh (second attempt): ", refreshedAccessToken);
    //                 headers['Authorization'] = `Bearer ${refreshedAccessToken}`;
    //                 const newOptionsWithToken = {
    //                     ...options,
    //                     headers: headers
    //                 };
    //                 return await fetch(url, newOptionsWithToken);  // Повторный запрос
    //             } else {
    //                 // Если второй раз не удалось обновить, перенаправляем
    //                 console.error('Second attempt to refresh token failed, redirecting to login');
    //                 window.location.href = '/app/templates/auth.html'; // Перенаправляем
    //                 return;
    //             }
    //         }
    //
    //         //  Если запрос успешен или возникла другая ошибка, просто возвращаем ответ
    //         return response;
    //
    //     } catch (error) {
    //         console.error('API request error:', error);
    //         throw error; // Пробрасываем ошибку дальше
    //     }
    // }


    // Пример использования: запрос к защищенному ресурсу
    // async function fetchData() {
    //     try {
    //         const response = await apiRequest('/api/protected-resource', { // Замените на ваш эндпоинт
    //             method: 'GET',
    //             headers: {
    //                 //  'Authorization': 'Bearer ' //  Access Token уже добавляется в apiRequest
    //             }
    //         });
    //
    //         if (!response.ok) {
    //             //  console.error('API request failed');
    //             return;
    //         }
    //
    //         const data = await response.json();
    //         console.log('Protected resource data:', data);
    //
    //     } catch (error) {
    //         // console.error('Fetch Data Error:', error);  //  Обрабатывается в apiRequest
    //         // Отобразите общую ошибку пользователю
    //     }
    // }
    async function logout() {
        console.log("logout() start");
        stopTokenRefreshInterval();
        console.log("Вызываем deleteCookie для access_token...");
        await deleteCookie('access_token'); // Удаляем Access Token
        console.log("Вызываем deleteCookie для refresh_token...");
        await deleteCookie('refresh_token'); // Удаляем Refresh Token
        console.log("Перенаправление на auth.html...");
        window.location.href = '../../../templates/auth/auth.html';
        console.log("logout() end");
    }

    // Функция для запуска таймера обновления токенов
    // setInterval(callback, delay): Функция setInterval принимает два аргумента:
    // callback: Функция, которая будет выполняться с заданным интервалом.
    // delay: Интервал в миллисекундах между вызовами функции callback.


    //  Запускаем автоматическое обновление токенов (при загрузке страницы, например)
    async function checkAuthentication() {
        const refresh_token = getCookie('refresh_token');
        if (refresh_token) {
            startTokenRefreshInterval();
        } else {
            window.location.href = '../../../templates/main_page/main_page.html';
            return;
        }
    }

    // checkAuthentication();

      // Замените 'logoutButton' на ID вашей кнопки
    if (logoutButton) {
        logoutButton.addEventListener('click',  async (event) => {
            await logout();
        });
    }

     // Обработчик отправки формы логина
    // if (loginButton) {
    //     loginForm.addEventListener('submit', async (event) => {  //  Слушаем 'submit' на форме
    //         event.preventDefault();  //  Предотвращаем отправку формы по умолчанию
    //     });
    // }

        // Event listener for login button
    if (loginButton) {
        loginButton.addEventListener('click', async (event) => {
            event.preventDefault();
            await login();
        });
    }



    // Event listener for register button
    if (registerButton) {
        registerButton.addEventListener('click', async (event) => {
            event.preventDefault();
            await register();
        });
    }

    // Функция для переключения между формами (если нужно)
    function flipToRegister() {
        const authViewContainer = document.getElementById('auth-view-container');
        if (authViewContainer) {
            authViewContainer.classList.add('flipped');
        }
    }

    function flipToLogin() {
        const authViewContainer = document.getElementById('auth-view-container');
        if (authViewContainer) {
            authViewContainer.classList.remove('flipped');
        }
    }

    // Event listener for "Создать" (переход к регистрации)
    if (registerLink) {
        registerLink.addEventListener('click', (event) => {
            event.preventDefault();
            flipToRegister();
        });
    }
    // Event listener for "Войти" (переход к логину)
    if (loginLink) {
        loginLink.addEventListener('click', (event) => {
            event.preventDefault();
            flipToLogin();
        });
    }

    //  Initial form
    flipToLogin();
});
