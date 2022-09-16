let inputag = document.querySelector('.inputag');
let hide = document.querySelector('.hide');


hide.addEventListener('click', ()=>{
    hide.classList.toggle('display')
    if(inputag.type=='password'){
    inputag.type= 'text'
}else{
    inputag.type='password'
}
})

// let input1 = document.querySelector('.input1');
// let hideme = document.querySelector('.hideme');


// hideme.addEventListener('click', ()=>{
//     hideme.classList.toggle('display')
//     if(inputag.type=='password'){
//     input1.type= 'text'
// }else{
//     input1.type='password'
// }
// })