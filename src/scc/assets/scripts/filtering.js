function search() {
    var input, filter, cards, article, title, i, titleValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    cards = document.getElementById("myCards");
    article = cards.getElementsByTagName("article");

    for (i = 0; i < article.length; i++) 
    {
        title = article[i].getElementsByClassName("title")[0];
        titleValue = title.textContent || title.innerText;
        if (titleValue.toUpperCase().indexOf(filter) > -1) { article[i].style.display = ""; } 
        else { article[i].style.display = "none"; }
    }
}

// Show cards
cards.forEach(element => {
    document.getElementById('myCards').innerHTML += element.html_card
});

