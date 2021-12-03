const username = document.getElementById('username').value
const email = document.getElementById('email').value
const phoneNumber = document.getElementById('phone_number').value
const totalCost = document.getElementById('total_cost').innerHTML
const checkoutBtn = document.getElementById('process_payment')


checkoutBtn.addEventListener('click', (e) => {
    console.log(username)
      e.preventDefault()

    console.log('Payment made', username)
    console.log('Email', email)
    console.log('Phone Number', phoneNumber)
    console.log('Total Cost', totalCost)

    FlutterwaveCheckout({
        public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
        tx_ref: "RX1",
        amount: totalCost,
        currency: "KES",
        country: "KENYA",
        payment_options: "MPESA",
        redirect_url: // specified redirect URL
          "/user/",
        meta: {
          consumer_id: '',
          consumer_mac: "92a3-912ba-1192a",
        },
        customer: {
          email: email,
          phone_number: phoneNumber,
          name: username,
        },
        callback: function (data) {
          console.log(data);
        },
        onclose: function() {
          // close modal
        },
        customizations: {
          title: "The Farm Ke",
          description: "Payment for items in cart",
          logo: "",
        },
      });
})


