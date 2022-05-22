
btns = document.getElementsByClassName('copy-btn');
for (let index = 0; index < btns.length; index++) {
    const element = btns[index];
    element.addEventListener('click', function () {
        console.log('copy btn!');
        for (let index = 0; index < cards.length; index++) {
            const card = cards[index];
            if(card.id == $(this).val()){
                navigator.clipboard.writeText(card.html_card_embedded);
                break;
            }
        }
    });
}

btns = document.getElementsByClassName('copy-citation-btn');
for (let index = 0; index < btns.length; index++) {
    const element = btns[index];
    element.addEventListener('click', function () {
        console.log('copy citation btn!');
        for (let index = 0; index < cards.length; index++) {
            const card = cards[index];
            if(card.id == $(this).val()){
                navigator.clipboard.writeText(card.citationText);
                break;
            }
        }
    });
}