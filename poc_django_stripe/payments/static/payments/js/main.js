
function subscription_purchase(url) {
  // Get Stripe publishable key
  fetch("/payments/config/")
  .then((result) => { return result.json(); })
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // Event handler
    fetch(url)
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
}


function subscription_cancel(url) {
  const msg = 'Are you sure you want to cancel your subscription?';
  confirm_message(url, msg);
}

function subscription_reactivate(url) {
  const msg = 'Are you sure you want to reactivate your subscription?';
  confirm_message(url, msg);
}
