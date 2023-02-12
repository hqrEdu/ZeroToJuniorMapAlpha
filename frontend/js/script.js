const input = document.querySelector('.form__discord-input');
const cityInput = document.querySelector('.form__city-input')
const cityText = 'Wpisz swoje miasto...'
const defaultText = 'Twój nick z Discord';

input.addEventListener('focus', function () {
    if (input.value === defaultText) {
        input.value = '';
    }
});

input.addEventListener('blur', function () {
    if (input.value === '') {
        input.value = defaultText;
    }
});
cityInput.addEventListener('focus', function () {
    if (cityInput.value === cityText) {
        cityInput.value = '';
    }
})

cityInput.addEventListener('blur', function () {
    if (cityInput.value === '') {
        cityInput.value = cityText;
    }
})



