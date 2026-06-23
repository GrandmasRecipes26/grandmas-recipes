const cart = JSON.parse(localStorage.getItem("cart")) || [];

let total = 0;

cart.forEach(item => {
    total += item.price * item.quantity;
});

localStorage.setItem("totalAmount", total);