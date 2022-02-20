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

const acknowledgement = document.getElementById('acknowledgement');
const citation = document.getElementById('citation');
const docker = document.getElementById('docker');
const documentation = document.getElementById('documentation');
const identifier = document.getElementById('identifier');
const download = document.getElementById('download');
const installation = document.getElementById('installation');
const license = document.getElementById('license');
const notebook = document.getElementById('notebook');
const paper = document.getElementById('paper');
const readme = document.getElementById('readme');

const title = document.getElementById('title');
const stars = document.getElementById('stars');
const releases = document.getElementById('releases');
const last_updated = document.getElementById('last_updated');


// Listeners
searchBar.addEventListener('keyup', () =>{ search(); })

acknowledgement.addEventListener('click', () =>{ state_acknowledgement = !state_acknowledgement; search(); })
citation.addEventListener('click', () =>{ state_citation = !state_citation; search(); })
docker.addEventListener('click', () =>{ state_docker = !state_docker; search(); })
documentation.addEventListener('click', () =>{state_documentation = !state_documentation; search(); })
identifier.addEventListener('click', () =>{ state_identifier = !state_identifier; search(); })
download.addEventListener('click', () =>{ state_download = !state_download; search(); })
installation.addEventListener('click', () =>{ state_installation = !state_installation; search(); })
license.addEventListener('click', () =>{ state_license = !state_license; search(); })
notebook.addEventListener('click', () =>{ state_notebook = !state_notebook; search(); })
paper.addEventListener('click', () =>{ state_paper = !state_paper; search(); })
readme.addEventListener('click', () =>{state_readme = !state_readme; search(); })

title.addEventListener('click', () =>{ state_title = true; state_stars = false; state_releases = false; state_last_updated = false; search(); })
stars.addEventListener('click', () =>{ state_title = false; state_stars = true; state_releases = false; state_last_updated = false; search(); })
releases.addEventListener('click', () =>{ state_title = false; state_stars = false; state_releases = true; state_last_updated = false; search(); })
last_updated.addEventListener('click', () =>{ state_title = false; state_stars = false; state_releases = false; state_last_updated = true; search(); })

// States
let state_acknowledgement = false;
let state_citation = false;
let state_docker = false;
let state_documentation = false;
let state_identifier = false;
let state_download = false;
let state_installation = false;
let state_license = false;
let state_notebook = false;
let state_paper = false;
let state_readme = false;

let state_title = false;
let state_stars = false;
let state_releases = false;
let state_last_updated = false;

// Search engine
function search() {

    const usr_query = searchBar.value.toLowerCase();
    const filteredCards = cards.filter(card => {
        return (card.title.toLowerCase().includes(usr_query) || card.description.toLowerCase().includes(usr_query))
            && ( 
                   ((state_acknowledgement)? card.acknowledgement : true) 
                && ((state_citation)? card.citation : true)
                && ((state_docker)? card.docker : true)
                && ((state_documentation)? card.documentation : true)
                && ((state_identifier)? card.identifier : true) 
                && ((state_download)? card.download : true)
                && ((state_license)? card.license : true)
                && ((state_notebook)? card.notebook : true)
                && ((state_paper)? card.paper : true)
                && ((state_readme)? card.readme : true)
                && ((state_installation)? card.installation : true));
    });

    // Order by
    ordered_cards = filteredCards.sort((a,b) => {
        if (state_title) {
            return (a.title > b.title)? 1 : -1;
        }
        if (state_stars) {
            return b.stars - a.stars;
        }
        if (state_releases) {
            return b.releases - a.releases;
        }
        if (state_last_updated) {
            return a.recently_updated - b.recently_updated;
        }
    });

    displayCards(ordered_cards);
}

const displayCards = (cards) => {
    const htmlString = cards
        .map((card) => {
            return card.html_card
        })
        .join('');
    document.getElementById('myCards').innerHTML = htmlString

    add_tooltip();
    add_copy_card();
}

loadCardsData();
