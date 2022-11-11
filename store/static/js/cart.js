var updateBtns = document.getElementsByClassName('update-cart');


for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action);
        
        if (user == 'AnonymousUser'){
            addCookieItem(productId,action);
            }else{
            updateUserOrder(productId, action);
            }
        
    })
    
}

function addCookieItem(productId,action){
    console.log('user not authenticated')

    if (action == 'add'){
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity':1};

            if (cart_no["cart_items"] == undefined) {
                cart_no["cart_items"] = 1;

            }else{
                cart_no["cart_items"] += 1;
            }
        }else{
            cart[productId]['quantity'] +=1;
        }
    }

    if (action == 'remove'){
        cart[productId]['quantity'] -= 1;
        cart_no["cart_items"] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            console.log('delete item')
            delete cart[productId];
        }

        if (cart_no["cart_items"] <= 0) {
            cart_no["cart_items"] = 0;
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    document.cookie = 'cartno=' + JSON.stringify(cart_no) + ";domain=;path=/";
    location.reload();
}

var cart_t = document.getElementsByClassName("cart-num");


// let product_no = parseInt(localStorage.getItem("cart_no"));

// if (product_no){
//     localStorage.setItem("cart_no", cart_no["cart_items"] + 1);
// }else{
//     localStorage.setItem("cart_no", cart_no["cart_items"]);
// }


// cart_t[0].children[0].innerHTML = localStorage.getItem("cart_no");





function updateUserOrder(productId, action){
                console.log('user logged in, sending data..');
                var url = '/update_item/';

                fetch(url, {
                    method:'POST',
                    headers: {
                        'Content-Type':'application/json',
                        'X-CSRFToken': csrftoken,
                    },
                    body:JSON.stringify({'productId': productId, 'action': action,})

                }).then(response =>{
                    return response.json();
                }).then(data => {
                    console.log('data:',data);
                    location.reload()
                })
}




// user nav menu functionality once logged in(user,profile,account,logout)
let user_drop_down = document.getElementsByClassName("user_drop_down")[0];
let user_menu = document.getElementsByClassName("user_menu")[0];


user_drop_down.addEventListener("click", function(){
    let menu_height = user_menu.getBoundingClientRect().height;

    if (menu_height < 10){
        // user_menu.classList.remove("hide-item");

        user_menu.style.height = "84px";
        user_drop_down.style.transform = 'rotate(0deg)';
        user_menu.classList.remove('user_menu_new');
        user_menu.classList.add('user_menu_old');
        
    }

    if (menu_height > 10){
        user_menu.style.height = "0";
        user_menu.style.top = "2.6rem";
        user_menu.classList.add('user_menu_new');
        user_drop_down.style.transform = 'rotate(-90deg)';
        
    }
    console.log(menu_height)

});



