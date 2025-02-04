function switchTab(id) {
    var header = $('.tab_header_item[data-tab="'+ Number(id) +'"]');
    var content = $('.tab_content_item[data-tab="'+ Number(id) +'"]');
    
    $('.tab_header_item.active').removeClass('active');
    header.addClass('active');
    
    $('.tab_content_item.active').removeClass('active');
    content.addClass('active');
}

function showSnackbar() {
    var snackbar = document.getElementById("snackbar");
    snackbar.className = "show";
    snackbar.innerText = "Данные были успешно отправлены!";
    setTimeout(function(){ 
        snackbar.className = snackbar.className.replace("show", "");
    }, 4000);
}