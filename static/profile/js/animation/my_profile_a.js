const myProfileButton= document.querySelector('.my-profile-button');
const settingsButton = document.getElementById('settings-button');
const helpButton = document.getElementById('help-button');

const dropdownContentProfile = document.querySelector('.dropdown-content-profile');


myProfileButton.addEventListener('click', () => {

    // toogle
    // Если у элемента dropdownContentProfile нет класса show-profile, то он добавляет этот класс к элементу.
    // Если у элемента dropdownContentProfile уже есть класс show-profile, то он удаляет этот класс из элемента.
    dropdownContentProfile.classList.toggle('show-profile');
});

// if (myProfileButton) {
//     myProfileButton.addEventListener('pointerdown', () => {
//         myProfileButton.classList.add('active'); // Добавляем класс active при нажатии
//     });
//
//     document.addEventListener('pointerup', (event) => {  // Слушаем mouseup на всем документе
//         if (myProfileButton.contains(event.target)) { // Проверяем, что клик был внутри кнопки
//             dropdownContentProfile.classList.toggle('show-profile'); // открываем меню только если кликнули по кнопке
//         }
//         myProfileButton.classList.remove('active'); // Всегда убираем класс active при отпускании
//     });
//
//     myProfileButton.addEventListener('pointerleave', () => {
//         myProfileButton.classList.remove('active'); // Убираем класс active, если курсор покинул кнопку
//     });
// }

if (dropdownContentProfile) {
    dropdownContentProfile.addEventListener('click', (event) => {
        event.stopPropagation();
    });
}

window.addEventListener('click', (event) => {
    // Если клик был не на кнопке, и выпадающий список открыт, закрываем его
    // contains проверяет, содержит ли элемент dropdownContent класс show-profile
    if (!event.target.closest('.my-profile-button') && dropdownContentProfile.classList.contains('show-profile')) {
        dropdownContentProfile.classList.remove('show-profile');
    }
});