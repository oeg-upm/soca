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
searchBar.addEventListener('keyup', () =>{
    search()
})

function search() {

    const usr_query = searchBar.value.toLowerCase();
    const fileredCards = cards.filter(card => {
        return card.title.toLowerCase().includes(usr_query) 
            || card.description.toLowerCase().includes(usr_query);
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
