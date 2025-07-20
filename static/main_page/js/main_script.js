import {initializeChannels} from "./channels.js";

// Получаем ссылки на кнопки (каналы, задачи, календарь)
const buttons = document.querySelectorAll('.main_buttons a');

// Получаем контейнер для контента
const contentContainer = document.querySelector('.content');

// function loadScript(url) {
//   return new Promise((resolve, reject) => {
//     const script = document.createElement('script');
//     script.src = url;
//     script.onload = resolve;
//     script.onerror = reject;
//     document.head.appendChild(script);
//   });
// }

// Обработчик клика по кнопке
function loadContent(url) {
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .then(html => {
            contentContainer.innerHTML = html; // Заменяем содержимое
            // После загрузки HTML, ищем ссылки на каналы и добавляем обработчики
            // const channelLinks = document.querySelectorAll('.channel-list a');
            // if (channelLinks) {
            //     channelLinks.forEach(link => {
            //         link.addEventListener('click', (event) => {
            //             event.preventDefault();
            //             const channel = link.dataset.channel;
            //             console.log(`Clicked on channel: ${channel}`);
            //             // Здесь ваш код обработки клика по каналу
            //             // ...
            //         });
            //     });
            // } else {
            //     console.warn("No channel links found after loading content.");
            // }
            // console.log('initializeChannels called');
            // loadScript("../static/js/main_page/channels.js").then(() => {
            initializeChannels();
            // });
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
            contentContainer.innerHTML = '<p>Ошибка загрузки контента.</p>'; // Отображаем сообщение об ошибке
        });
}

// Добавляем обработчики событий к кнопкам
buttons.forEach(button => {
    button.addEventListener('click', (event) => {
        event.preventDefault(); // Предотвращаем переход по ссылке
        const targetUrl = button.getAttribute('href'); // Получаем URL из href атрибута
        loadContent(targetUrl);
    });
});

