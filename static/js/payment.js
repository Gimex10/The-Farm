const username = document.getElementById('username').value
const email = document.getElementById('email').value
const phoneNumber = document.getElementById('phone_number')
const personalAddress = document.querySelector('.personal-address')
const streetName = document.querySelector('.street-name')
const roadName = document.querySelector('.road-name')
const orderNumber = document.getElementById('order_number').innerHTML
const totalCost = document.getElementById('total_cost').innerHTML
const checkoutBtn = document.getElementById('process_payment')


checkoutBtn.addEventListener('click', (event) => {
    event.preventDefault()


    FlutterwaveCheckout({
        public_key: "FLWPUBK_TEST-SANDBOXDEMOKEY-X",
        tx_ref: "RX1",
        amount: totalCost,
        currency: "KES",
        country: "KENYA",
        payment_options: "MPESA",
        redirect_url: // specified redirect URL
          `/success/${orderNumber}/`,
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


