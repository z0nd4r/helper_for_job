import {ENDPOINTS} from './config.js';
import {userInfo} from "../../profile/js/my_profile.js";
// import {stopTokenRefreshInterval} from "./script";

// Функция для обработки логина
export async function login() {
    const username = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const loginError = document.getElementById('auth-error');

    // убрать предыдущие сообщения об ошибках
    loginError.textContent = '';
    console.log('Hello')
    if (username === '' || password === '') {
        loginError.textContent = 'Ошибка: некоторые из полей пусты';
        throw new Error('Ошибка: некоторые из полей пусты')
    }

    try {
        // console.log('Hello')
        // получение данных из формы
        const formData = new FormData();
        formData.append("username", username);
        formData.append("password", password);

        const response = await fetch(ENDPOINTS.login, {
            method: 'POST',
            credentials: 'include', // **Отправлять cookie**
            body: formData, //  Отправляем FormData, а не JSON
        });

        if (!response.ok) {
            // Получаем текст ошибки
            const errorText = await response.json(); // Получаем тело ответа
            console.log("Response text:", errorText.detail.message);
            // Формируем сообщение об ошибке
            const errorMessage = errorText.detail.message || `Login failed: некоторые из полей пусты`;
            throw new Error(errorMessage); // Выбрасываем исключение с сообщением об ошибке
        }

        const logText = await response.json();

        window.location.href = '../../../app/templates/main_page/main_page.html';



        console.log('Tokens:', logText);
        //  Токены установлены в куки бэкендом
        //  console.log('Login success, tokens set in cookies');  //Перенаправляем

    } catch (error) {
        console.error('Login error:', error);
        loginError.textContent = error.message;
    }
}

// Функция для обработки регистрации
export async function register() {
    const username = document.getElementById('register-username').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const registerError = document.getElementById('auth-error');

    registerError.textContent = '';

    if (username === '' || email === '' || password === '') {
        registerError.textContent = 'Ошибка: некоторые из полей пусты';
        throw new Error('Ошибка: некоторые из полей пусты')
    }



    try {
        const formData = new FormData();
        formData.append("username", username);
        formData.append("email", email)
        formData.append("password", password);

        const response = await fetch(ENDPOINTS.register, {
            method: 'POST',
            credentials: 'include', // **Отправлять cookie**
            body: formData
            // headers: {
            //     'Content-Type': 'application/json'
            // },
            // body: JSON.stringify({username, email, password})
        });

        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            console.log(response);
            throw new Error(data.detail.message || `Registration failed: ${response.status}`);
        }

        //console.log('Registration success');
        window.location.href = '../../../app/templates/main_page/main_page.html';
    } catch (error) {
        console.error('Registration error:', error);
        registerError.textContent = error.message;
    }
}

// export async function logout(){
//     stopTokenRefreshInterval()
//     window.location.href = '/app/templates/auth.html'
// }

