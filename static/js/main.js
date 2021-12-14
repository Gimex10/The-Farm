// Get all date input from DOM
const calenders = document.querySelectorAll('.dateinput')
const usernameElement = document.getElementById('id_customer')
const orderElement = document.getElementById('id_order')
const submitBtn = document.getElementById('cancel-order')
const dialogBox = document.getElementById('dialog-box')
const backBtn = document.querySelector('.back-btn')


// Event Listeners

// })

if(usernameElement){
usernameElement.addEventListener('mousedown', (e) => {
    e.preventDefault()
})

}
if(orderElement){
orderElement.addEventListener('mousedown', (e) => {
    e.preventDefault()
})

}

if(submitBtn){
    submitBtn.addEventListener('click', (e) => {
        console.log('Order Cancelled')
        dialogBox.style.display = 'block'
    })

    backBtn.addEventListener('click', (e) =>{
        dialogBox.style.display = 'none'


    })
}


// Loop through all and change input type to date
for(let i=0; i < calenders.length; i ++){
    calenders[i].setAttribute("type", "date")
        
}

