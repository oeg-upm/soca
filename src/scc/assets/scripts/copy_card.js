("button").click(function() {
    var copy_card = document.getElementById($(this).val());
    navigator.clipboard.writeText(copy_card.outerHTML)    
});
