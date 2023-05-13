const menu = document.querySelector('#carteira');
const carteira = document.querySelector('.carteira');

menu.addEventListener('click', function(){
    carteira.classList.toggle('ativo');
});


