let body = document.querySelector('body');
let flip = document.querySelector('.flip');
let fmoon = document.querySelector('.fa-moon');


flip.addEventListener('click', ()=>{
    body.classList.toggle('dark')
    if(body.classList.contains('dark')){
        fmoon.classList.replace('fa-moon', 'fa-sun')
    }else{
        fmoon.classList.replace('fa-sun', 'fa-moon')
    }
})