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
window.addEventListener('click', (event) => {
    if (!event.target.matches('.my-profile-button')) {
        // contains проверяет, содержит ли элемент dropdownContent класс show-profile
        if (dropdownContent.classList.contains('show-profile')) {
            dropdownContent.classList.remove('show-profile');
        }
    }
});