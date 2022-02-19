/*var xhReq = new XMLHttpRequest();
xhReq.open("GET", "cards_data.json", false);
xhReq.send(null);
var cards = JSON.parse(xhReq.responseText);
*/
// Load cards data
let cards = [];
const loadCardsData = async () => {
    try {
        const res = await fetch('cards_data.json');
        cards = await res.json();
        displayCards(cards);
    } catch (error) {
        console.error(error);
    }
}

// References
const searchBar = document.getElementById('searchBar');

// Listeners
searchBar.addEventListener('keyup', (e) =>{
    search()
})

function search() {
    // searchBar.value gets query text
    const fileredCards = cards.filter(card => {
        return card.title.includes(searchBar.value) || card.description.includes(searchBar.value);
    });
    // Order by title
    //ordered_cards = cards.sort((a,b) => (a.title > b.title)? 1 : -1);

    console.log(fileredCards);
    displayCards(fileredCards);
}

const displayCards = (cards) => {
    const htmlString = cards
        .map((card) => {
            return card.html_card
        })
        .join('');
    document.getElementById('myCards').innerHTML = htmlString
}

loadCardsData();
