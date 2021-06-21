$(document).on("click", ".customer-row", function() {
    var path   = window.location.href;
    id_num = $(this)[0].children[2].innerText //gets issuing-authority
    url = path + "/customer-edit?customer_id=" + id_num;
    window.location = url;
});