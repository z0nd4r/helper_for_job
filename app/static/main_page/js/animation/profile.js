const profileButton = document.querySelector('.profile-button');
const dropdownContent = document.querySelector('.dropdown-content');


profileButton.addEventListener('click', () => {
    dropdownContent.classList.toggle('show');
});

// Закрываем выпадающее меню при клике вне его
window.addEventListener('click', (event) => {
    if (!event.target.matches('.profile-button') &&
        !event.target.matches('.no-close')) { // Добавляем исключение для кнопок с классом no-close
            if (dropdownContent.classList.contains('show')) {
                dropdownContent.classList.remove('show');
            }
    }
});