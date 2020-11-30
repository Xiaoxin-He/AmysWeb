// let carts = document.querySelectorAll('.add-cart');




// console.log(total_items);
// var elem = document.getElementById('length').innerHTML;
// console.log("my loop" + elem);



var total_p_names = [];
// for (let i = 0; i < carts.length; i++) {
//     var tm1 = document.getElementById('product-name');
// }


function myfunction(index) {



    p_name = document.getElementById('product-name-' + index).innerHTML;
    // console.log(p_name);

    p_description = document.getElementById('product-description-' + index).innerHTML;
    // console.log(p_des);

    p_id = document.getElementById('product-id-' + index).innerHTML;
    console.log("id = ", p_id);

    p_price = document.getElementById('product-price-' + index).innerHTML;
    let p_image = document.getElementById('product-image-' + index).src;

    // p_image = document.getElementById('product-image-' + index).innerHTML;
    let products = [{
        product_id: p_id,
        name: p_name,
        tag: p_description,
        price: p_price,
        inCart: 0,
        image: p_image
    }]

    // console.log("p", products[0]);
    // console.log("w p", products);

    totalCost(products);
    cartNumbers(products);

    // setItems(products);
    console.log(p_image);

    localStorage.setItem("product_img", p_image)

    displayCart(p_image);

}


function onLoadCartNumbers() {
    let productNumbers = localStorage.getItem('cartNumbers');
    console.log("current number", productNumbers);
    if (productNumbers) {
        document.querySelector('.cart span').textContent = productNumbers;
    }
}
//pass the cart_num to localstorage
function cartNumbers(product, action) {

    // console.log("the product clicked is", product);
    let productNumbers = localStorage.getItem('cartNumbers');

    //convert string into numbers, should be int not float
    productNumbers = parseInt(productNumbers);

    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    //have sth in the cart
    if (action) {
        localStorage.setItem("cartNumbers", productNumbers - 1);
        document.querySelector('.cart span').textContent = productNumbers - 1;
        console.log("action running", productNumbers);
    } else if (productNumbers) {
        localStorage.setItem('cartNumbers', productNumbers + 1);
        document.querySelector('.cart span').textContent = productNumbers + 1;
    } else {
        localStorage.setItem('cartNumbers', 1);
        document.querySelector('.cart span').textContent = 1;
    }



    // let currentProduct = product[0].name;
    // console.log("currentProduct is", currentProduct);

    setItems(product);
}

function setItems(product, currentProduct) {


    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    if (cartItems != null) {
        // console.log(cartItems[product[0].name]); --undefine first



        let currentProduct = product[0].name;
        console.log("currentProduct is", currentProduct);

        if (cartItems[currentProduct] == undefined) {
            cartItems = {
                ...cartItems,
                [product[0].name]: product[0]
            }

        }
        cartItems[product[0].name].inCart += 1;
        //cake 1

    } else {
        product[0].inCart = 1;
        cartItems = {
            [product[0].name]: product[0]
        }

    }

    // console.log(cartItems);
    // console.log([product[0].inCart]);

    localStorage.setItem("productsInCart", JSON.stringify(cartItems));
}

function totalCost(product, action) {
    // console.log("hello", product[0].price);
    // localStorage.setItem("totalCost", product[0].price);
    let cartCost = localStorage.getItem('totalCost');
    console.log("My cart cost is", cartCost);

    if (action) {

        cartCost = parseFloat(cartCost); //should be float!
        let totalcost = parseFloat(cartCost) - parseFloat(product[0].price);
        localStorage.setItem("totalCost", totalcost);

    } else if (cartCost != null) {
        cartCost = parseFloat(cartCost);
        let totalcost = parseFloat(cartCost) + parseFloat(product[0].price);
        localStorage.setItem("totalCost", parseFloat(totalcost));

    } else {
        localStorage.setItem("totalCost", product[0].price);
    }
}


function displayCart(image) {
    // var p_image = document.getElementById('product-name-' + index).innerHTML;
    var i = image;
    let cartItems = localStorage.getItem("productsInCart");
    cartItems = JSON.parse(cartItems);
    let productContainer = document.querySelector(".products");
    let cartCost = localStorage.getItem('totalCost');


    let current_image = localStorage.getItem("product_img");
    // <img src="{{ url_for('upload', filename='cake2.jpeg') }}" style="width: 300px"></img>


    // console.log(current_image);
    // console.log(image);
    if (cartItems && productContainer) {
        productContainer.innerHTML = ''; //no repeat
        Object.values(cartItems).map(items => {
            productContainer.innerHTML += `
            <div class="product">
                <ion-icon name="trash-outline"></ion-icon>
                <img src="${items.image}">
                <span class="sm-hide" id="p_name">${items.name}</span>
             </div>
             <div class = "price sm-hide" id="p_price">$${items.price}</div>
             <div class = "quantity">
                 <ion-icon class="decrease" name="caret-back-circle-outline"></ion-icon>
                 <span>${items.inCart}</span>
                 <ion-icon class="increase" name="caret-forward-circle-outline"></ion-icon>
             </div>
             <div class= "total">
                $${items.inCart * items.price}
             </div>
            `;
        });

        productContainer.innerHTML += `
            <div class="basketTotalContainer">
                <h4 class="basketTotalTitle">
                    Basket Total
                </h4>
                <h4 class="basketTotal">
                    $${cartCost}
                </h4>
            </div>
        `
        deleteButtons();
        manageQuantity();
    }
}

function deleteButtons() {
    let deleteButtons = document.querySelectorAll('.product ion-icon');
    let productNumbers = localStorage.getItem('cartNumbers');
    let cartCost = localStorage.getItem("totalCost");
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);
    let productName;
    console.log(cartItems);
    // console.log("hello")

    for (let i = 0; i < deleteButtons.length; i++) {
        deleteButtons[i].addEventListener('click', () => {
            productName = deleteButtons[i].parentElement.textContent.toLocaleLowerCase().replace(/ /g, '').trim();


            localStorage.setItem('cartNumbers', productNumbers - cartItems[productName].inCart);
            localStorage.setItem('totalCost', cartCost - (cartItems[productName].price * cartItems[productName].inCart));

            delete cartItems[productName];
            localStorage.setItem('productsInCart', JSON.stringify(cartItems));

            displayCart();
            onLoadCartNumbers();
        })
    }
}

function manageQuantity() {
    let decreaseButtons = document.querySelectorAll('.decrease');
    let increaseButtons = document.querySelectorAll('.increase');
    let currentQuantity = 0;
    let currentProduct = '';
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);
    console.log("current cartiTEMS", cartItems);


    for (let i = 0; i < increaseButtons.length; i++) {

        decreaseButtons[i].addEventListener('click', () => {
            console.log(cartItems); //can decrease the product number
            currentQuantity = decreaseButtons[i].parentElement.querySelector('span').textContent;
            console.log(currentQuantity);
            currentProduct = decreaseButtons[i].parentElement.previousElementSibling.previousElementSibling.querySelector('span').textContent.toLocaleLowerCase().replace(/ /g, '').trim();
            // console.log("current product", currentProduct); //cake2
            // console.log("cartitems", cartItems);
            // console.log("cartitems with currentProduct ", cartItems[currentProduct]);
            console.log("try get item  2222", cartItems[currentProduct].name);


            if (cartItems[currentProduct].inCart > 1) {
                cartItems[currentProduct].inCart -= 1; //can read
                let cartCost = localStorage.getItem("totalCost");
                let gotItem = localStorage.getItem("currentItemiN");
                // console.log("check current product in cart", gotItem);
                // console.log("get lenght of", Object.keys(cartItems).length);


                var current_total_price = 0;
                for (var key in cartItems) {
                    var item = cartItems[key];
                    current_total_price += item["price"] * item["inCart"];
                }


                localStorage.setItem('totalCost', current_total_price);


                localStorage.setItem('productsInCart', JSON.stringify(cartItems));


                displayCart();
            }

        });

        increaseButtons[i].addEventListener('click', () => {
            // console.log(cartItems);
            currentQuantity = increaseButtons[i].parentElement.querySelector('span').textContent;
            // console.log(currentQuantity);
            currentProduct = increaseButtons[i].parentElement.previousElementSibling.previousElementSibling.querySelector('span').textContent.toLocaleLowerCase().replace(/ /g, '').trim();
            // console.log(currentProduct);

            cartItems[currentProduct].inCart += 1;


            var current_total_price = 0;
            for (var key in cartItems) {
                var item = cartItems[key];
                current_total_price += item["price"] * item["inCart"];
            }


            localStorage.setItem('totalCost', current_total_price);

            localStorage.setItem('cartNumbers', cartItems[currentProduct].inCart);
            localStorage.setItem('productsInCart', JSON.stringify(cartItems)); //good
            displayCart();
        });
    }
}




function checkoutFunction() {
    let cartItems = localStorage.getItem('productsInCart');
    cartItems = JSON.parse(cartItems);

    fetch('http://localhost:5000/checkout/shirley1', {
            method: 'POST',
            body: JSON.stringify(cartItems),
            headers: {
                'Content-type': 'application/json; charset=UTF-8'
            }
        })
        .then(response => response.json())
        .then(json => {
            console.log(json);
        });

}



onLoadCartNumbers();
displayCart();