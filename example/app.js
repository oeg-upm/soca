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
const requirements = document.getElementById('requirements');
const paper = document.getElementById('paper');

const title = document.getElementById('title');
const stars = document.getElementById('stars');
const releases = document.getElementById('releases');
const last_updated = document.getElementById('last_updated');


// Listeners
searchBar.addEventListener('keyup', () => { search(); })

acknowledgement.addEventListener('click', () => { 
    state_acknowledgement = !state_acknowledgement;  
    if (state_acknowledgement)
        acknowledgement.classList.add("filter-selected");
    else acknowledgement.classList.remove("filter-selected");
    search(); 
});

citation.addEventListener('click', () => { 
    state_citation = !state_citation; 
    if (state_citation)
        citation.classList.add("filter-selected");
    else citation.classList.remove("filter-selected");
    search(); 
});

docker.addEventListener('click', () => { 
    state_docker = !state_docker; 
    if (state_docker)
        docker.classList.add("filter-selected");
    else docker.classList.remove("filter-selected");
    search(); 
});

documentation.addEventListener('click', () => {
    state_documentation = !state_documentation;
    if (state_documentation)
        documentation.classList.add("filter-selected");
    else documentation.classList.remove("filter-selected");
    search(); 
});

identifier.addEventListener('click', () => { 
    state_identifier = !state_identifier;
    if (state_identifier)
        identifier.classList.add("filter-selected");
    else identifier.classList.remove("filter-selected");
    search(); 
});

download.addEventListener('click', () => { 
    state_download = !state_download;
    if (state_download)
        download.classList.add("filter-selected");
    else download.classList.remove("filter-selected");
    search(); 
});

installation.addEventListener('click', () => { 
    state_installation = !state_installation;
    if (state_installation)
        installation.classList.add("filter-selected");
    else installation.classList.remove("filter-selected");
    search(); 
});

license.addEventListener('click', () =>{ 
    state_license = !state_license; 
    if (state_license)
        license.classList.add("filter-selected");
    else license.classList.remove("filter-selected");
    search(); 
});

notebook.addEventListener('click', () => { 
    state_notebook = !state_notebook;
    if (state_notebook)
        notebook.classList.add("filter-selected");
    else notebook.classList.remove("filter-selected");
    search(); 
});
requirements.addEventListener('click', () => { 
    state_requirements = !state_requirements;
    if (state_requirements)
        requirements.classList.add("filter-selected");
    else requirements.classList.remove("filter-selected");
    search(); 
});
paper.addEventListener('click', () => { 
    state_paper = !state_paper; 
    if (state_paper)
        paper.classList.add("filter-selected");
    else paper.classList.remove("filter-selected");
    search(); 
});

title.addEventListener('click', () => { 
    state_title = !state_title; state_stars = false; state_releases = false; state_last_updated = false; 
    if (state_title){ title.classList.add("filter-selected"); }
    else { title.classList.remove("filter-selected"); }
    stars.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    search(); 
}); 

stars.addEventListener('click', () => { 
    state_title = false; state_stars = !state_stars; state_releases = false; state_last_updated = false; 
    if (state_stars){ stars.classList.add("filter-selected"); }
    else { stars.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    search(); 
}); 
releases.addEventListener('click', () => { 
    state_title = false; state_stars = false; state_releases = !state_releases; state_last_updated = false; 
    if (state_releases){ releases.classList.add("filter-selected"); }
    else { releases.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    stars.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    search(); 
});

last_updated.addEventListener('click', () => { 
     state_title = false; state_stars = false; state_releases = false; state_last_updated = !state_last_updated; 
    if (state_last_updated){ last_updated.classList.add("filter-selected"); }
    else { last_updated.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    stars.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    search(); 
}); 

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
let state_requirements = false;
let state_paper = false;

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
                && ((state_documentation)? card.hasDocumentation : true)
                && ((state_identifier)? card.identifier : true) 
                && ((state_download)? card.downloadUrl : true)
                && ((state_license)? card.license : true)
                && ((state_notebook)? card.notebook : true)
                && ((state_paper)? card.paper : true)
                && ((state_requirements)? card.requirements : true)
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
    add_modals();
}

function add_modals() {
    cards_icons_list = document.getElementsByClassName('ref-repo-icons');
    for(const cards_icons of cards_icons_list){
        for(const card_icon of cards_icons.children){
            const icon = card_icon.getElementsByClassName('icon')[0];
            const modal = card_icon.getElementsByClassName('modal')[0];
            const span_close = card_icon.getElementsByClassName('close')[0];
            if (modal != undefined){
                icon.addEventListener('click', () => { 
                    modal.classList.add('modal-on');
                });
                span_close.addEventListener('click', () => { 
                    modal.classList.remove('modal-on');
                });
            }
        }
    }
    
}


loadCardsData();
