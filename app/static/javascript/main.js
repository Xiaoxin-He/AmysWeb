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


    p_price = document.getElementById('product-price-' + index).innerHTML;
    let p_image = document.getElementById('product-image-' + index).src;

    // p_image = document.getElementById('product-image-' + index).innerHTML;
    let products = [{
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
                <span class="sm-hide">${items.name}</span>
             </div>
             <div class = "price sm-hide">$${items.price}</div>
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
    // let productName = cartItems[currentProduct];


    // console.log("hello manage" + decreaseButtons);\\
    // cartItems[product[0].name]
    // cartItems
    // x = cartItems;
    console.log("try get item", cartItems);
    // for (i = 0; i < cartItems.name.length; i++) {
    //     x += myObj.cars[i] + "<br>";
    // }




    // if (Object.keys(cartItems).length == 1) {
    //     console.log("the first item in cart");
    //     localStorage.setItem('currentItemiN', currentProduct);


    // } else {

    //     let gotItem = localStorage.getItem("currentItemiN");
    //     console.log("there are one than one item in the cart");
    //     console.log("has item", gotItem);

    // }

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
                console.log("check current product in cart", gotItem);
                console.log("get lenght of", Object.keys(cartItems).length);

                // cartNumbers(cartItems[currentProduct], "decrease");
                // totalCost(cartItems[currentProduct], "decrease");

                // console.log("totalcost of p", cartCost);
                // console.log(" decrease items.inCart", cartItems[currentProduct].inCart);
                // console.log(' decrease items.price total', cartItems[currentProduct].price * cartItems[currentProduct].inCart);

                localStorage.setItem('totalCost', cartItems[currentProduct].price * cartItems[currentProduct].inCart);

                localStorage.setItem('cartNumbers', cartItems[currentProduct].inCart);
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

            // cartNumbers(cartItems[currentProduct]);
            // totalCost(cartItems[currentProduct]);

            // console.log(" Increase items.inCart", cartItems[currentProduct].inCart); //good
            // console.log(" Increase items.price total", cartItems[currentProduct].price * cartItems[currentProduct].inCart);


            // console.log("can i get total name of prouct?", cartItems[currentProduct]);

            localStorage.setItem('totalCost', cartItems[currentProduct].price * cartItems[currentProduct].inCart);

            localStorage.setItem('cartNumbers', cartItems[currentProduct].inCart);
            localStorage.setItem('productsInCart', JSON.stringify(cartItems)); //good
            displayCart();
        });
    }
}







onLoadCartNumbers();
displayCart();