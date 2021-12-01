// Get all date input from DOM
const calenders = document.querySelectorAll('.dateinput')
const today = Date.now()


// const dateInputChange = (inputForm) =>{
// inputForm.addEventlistener('onsubmit', (e) => {
//     e.preventDefault()
//     const typedDate = inputForm.value
//     console.log('Saving Form', inputForm)
//     console.log('Typed Date', typedDate)

//     if( typedDate )
//     { 
//       alert("validation failed false");
//       returnToPreviousPage();
//       return false;
//     }
  
//     alert("validations passed");
//     return true;
//     // calenders[i].valueAsDate =  Date.now().toDateInputValue()
//     // console.log(calenders[i].value)
    
// })
    
//     }

// Loop through all and change input type to date
for(let i=0; i < calenders.length; i ++){
    calenders[i].setAttribute("type", "date")
    // dateInputChange(calenders[i])

    
}

