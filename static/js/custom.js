
document.querySelectorAll('a.nav-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault(); // Отменяем стандартное поведение ссылки
        const targetId = this.getAttribute('href').substring(1); // Убираем символ #
        const targetElement = document.getElementById(targetId); // Находим целевой элемент
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth', // Плавная прокрутка
            });
        }
    });
});

function openContactForm() {
    alert('Спасибо за ваш интерес! Мы свяжемся с вами в ближайшее время.');
}

function showMore(service) {
    let message = '';
    switch (service) {
        case 'montage':
            message = 'Мы выполняем монтаж высотных конструкций с использованием современных технологий и оборудования.';
            break;
        case 'repair':
            message = 'Наши специалисты качественно выполнят ремонт фасадов с гарантией надежности.';
            break;
        case 'cleaning':
            message = 'Очистка крыш от снега и льда проводится с соблюдением всех норм безопасности.';
            break;
    }
    alert(message);
}
