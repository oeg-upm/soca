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

// Pagination vars
let current_page = 1;
let cards_per_page = 12;

// References
const myCards = document.getElementById('myCards');
const searchBar = document.getElementById('searchBar');

const acknowledgement = document.getElementById('acknowledgement');
const citation = document.getElementById('citation');
const docker = document.getElementById('docker');
const documentation = document.getElementById('documentation');
const identifier = document.getElementById('identifier');
const status_let = document.getElementById('status');
const download = document.getElementById('download');
const installation = document.getElementById('installation');
const license = document.getElementById('license');
const notebook = document.getElementById('notebook');
const requirements = document.getElementById('requirements');
const usage = document.getElementById('usage');
const help = document.getElementById('help');
const paper = document.getElementById('paper');
const web = document.getElementById('web');
const ontology = document.getElementById('ontology');

const title = document.getElementById('title');
const stars = document.getElementById('stars');
const releases = document.getElementById('releases');
const last_updated = document.getElementById('last_updated');

const pagination = document.getElementById('pagination');

const owner = document.getElementById("owner");

// Listeners
searchBar.addEventListener('keyup', () => { current_page = 1; search(); })

acknowledgement.addEventListener('click', () => { 
    state_acknowledgement = !state_acknowledgement;  
    if (state_acknowledgement)
        acknowledgement.classList.add("filter-selected");
    else acknowledgement.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

citation.addEventListener('click', () => { 
    state_citation = !state_citation; 
    if (state_citation)
        citation.classList.add("filter-selected");
    else citation.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

docker.addEventListener('click', () => { 
    state_docker = !state_docker; 
    if (state_docker)
        docker.classList.add("filter-selected");
    else docker.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

documentation.addEventListener('click', () => {
    state_documentation = !state_documentation;
    if (state_documentation)
        documentation.classList.add("filter-selected");
    else documentation.classList.remove("filter-selected");
    current_page = 1;
    search();
});

identifier.addEventListener('click', () => { 
    state_identifier = !state_identifier;
    if (state_identifier)
        identifier.classList.add("filter-selected");
    else identifier.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
status_let.addEventListener('click', () => { 
    state_status = !state_status;
    if (state_status)
        status_let.classList.add("filter-selected");
    else status_let.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

download.addEventListener('click', () => { 
    state_download = !state_download;
    if (state_download)
        download.classList.add("filter-selected");
    else download.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

installation.addEventListener('click', () => { 
    state_installation = !state_installation;
    if (state_installation)
        installation.classList.add("filter-selected");
    else installation.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

license.addEventListener('click', () =>{ 
    state_license = !state_license; 
    if (state_license)
        license.classList.add("filter-selected");
    else license.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

notebook.addEventListener('click', () => { 
    state_notebook = !state_notebook;
    if (state_notebook)
        notebook.classList.add("filter-selected");
    else notebook.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
requirements.addEventListener('click', () => { 
    state_requirements = !state_requirements;
    if (state_requirements)
        requirements.classList.add("filter-selected");
    else requirements.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
usage.addEventListener('click', () => { 
    state_usage = !state_usage;
    if (state_usage)
        usage.classList.add("filter-selected");
    else usage.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
help.addEventListener('click', () => { 
    state_help = !state_help;
    if (state_help)
        help.classList.add("filter-selected");
    else help.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
paper.addEventListener('click', () => { 
    state_paper = !state_paper; 
    if (state_paper)
        paper.classList.add("filter-selected");
    else paper.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
web.addEventListener('click', () => { 
    state_web = !state_web; 
    if (state_web)
        web.classList.add("filter-selected");
    else web.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});
ontology.addEventListener('click', () => { 
    state_ontology = !state_ontology; 
    if (state_ontology)
        ontology.classList.add("filter-selected");
    else ontology.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

title.addEventListener('click', () => { 
    state_title = !state_title; state_stars = false; state_releases = false; state_last_updated = false; 
    if (state_title){ title.classList.add("filter-selected"); }
    else { title.classList.remove("filter-selected"); }
    stars.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    current_page = 1;
    search(); 
}); 

stars.addEventListener('click', () => { 
    state_title = false; state_stars = !state_stars; state_releases = false; state_last_updated = false; 
    if (state_stars){ stars.classList.add("filter-selected"); }
    else { stars.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    current_page = 1;
    search(); 
}); 
releases.addEventListener('click', () => { 
    state_title = false; state_stars = false; state_releases = !state_releases; state_last_updated = false; 
    if (state_releases){ releases.classList.add("filter-selected"); }
    else { releases.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    stars.classList.remove("filter-selected");
    last_updated.classList.remove("filter-selected");
    current_page = 1;
    search(); 
});

last_updated.addEventListener('click', () => { 
     state_title = false; state_stars = false; state_releases = false; state_last_updated = !state_last_updated; 
    if (state_last_updated){ last_updated.classList.add("filter-selected"); }
    else { last_updated.classList.remove("filter-selected"); }
    title.classList.remove("filter-selected");
    stars.classList.remove("filter-selected");
    releases.classList.remove("filter-selected");
    current_page = 1;
    search(); 
}); 

document.addEventListener('input', function (event) {

    // Only run on our select menu
    if (event.target.id !== 'owner') return;
    current_page = 1;
    search();

}, false);

// States
let state_acknowledgement = false;
let state_citation = false;
let state_docker = false;
let state_documentation = false;
let state_identifier = false;
let state_status = false;
let state_download = false;
let state_installation = false;
let state_license = false;
let state_notebook = false;
let state_requirements = false;
let state_usage = false;
let state_help = false;
let state_paper = false;
let state_web = false;
let state_ontology = false;

let state_title = false;
let state_stars = false;
let state_releases = false;
let state_last_updated = false;

// Search engine
function search() {

    const usr_query = searchBar.value.toLowerCase();
    const filteredCards = cards.filter(card => {
        return (card.name.toLowerCase().includes(usr_query) || card.description.toLowerCase().includes(usr_query))
            && ( 
                   ((state_acknowledgement)? card.acknowledgement : true) 
                && ((state_citation)? card.citation : true)
                && ((state_docker)? card.hasBuildFile : true)
                && ((state_documentation)? card.hasDocumentation : true)
                && ((state_identifier)? card.hasIdentifier : true)
                && ((state_status)? card.repoStatus : true) 
                && ((state_download)? card.downloadUrl : true)
                && ((state_license)? card.license : true)
                && ((state_notebook)? card.hasExecutableNotebook : true)
                && ((state_paper)? card.paper : true)
                && ((state_ontology)? card.isOntology : true)
                && ((state_web)? card.isWeb : true)
                && ((state_requirements)? card.requirement : true)
                && ((state_usage)? card.usage : true)
                && ((state_help)? card.help : true)
                && ((state_installation)? card.installation : true)
                )
            &&
                (
                    owner == undefined || card.owner == owner.value || 'all' == owner.value
                );
    });

    // Order by
    ordered_cards = filteredCards.sort((a,b) => {
        if (state_title) {
            return (a.name > b.name)? 1 : -1;
        }
        if (state_stars) {
            return b.stargazersCount - a.stargazersCount;
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

    let n_pages = Math.ceil(cards.length / cards_per_page);

    // Ensure that we are in a valid page
    current_page = Math.min(current_page, n_pages);
    current_page = Math.max(current_page, 1);
    
    // Build pagination numbers
    if (current_page != 1){
        pagination.innerHTML = '<span id="prev-page" style="cursor: pointer;"> < </span>';
    } else {pagination.innerHTML = ''}
    for (let i_page = 1; i_page <= n_pages; i_page++) {
        if(i_page == 1 || Math.abs(i_page - current_page) <=1 || i_page == n_pages){
            page = '<span id="'+i_page+'" style="cursor: pointer;">'+i_page +' </span>';
            if (i_page == current_page){
                page = '<b>'+page+'</b>';
            }
            if (i_page == 1 && current_page >= 4) {
                page += ' ... ';
            }
            if (i_page == n_pages && current_page <= n_pages-3) {
                page = ' ... ' + page;
            }
            pagination.innerHTML += page;
        }
    }
    if (current_page != n_pages){
       pagination.innerHTML += '<span id="next-page" style="cursor: pointer;"> > </span>'; 
    }
    if (n_pages == 0 || n_pages == 1){
        pagination.innerHTML = '<b style="cursor: pointer;" >1</b>';
    }
    for (let i_page = 1; i_page <= n_pages; i_page++) {
        ref = document.getElementById(''+i_page);
        if(ref != undefined){
            ref.addEventListener('click', () => {
                current_page = i_page;
                search();
            });
        }
    }
    ref_prev = document.getElementById('prev-page');
    if(ref_prev != undefined){
        ref_prev.addEventListener('click', () => {
            current_page = Math.max(current_page-1, 1);
            search();
        });
    }
    ref_next = document.getElementById('next-page');
    if(ref_next != undefined){
        ref_next.addEventListener('click', () => {
            current_page = Math.min(current_page+1, n_pages);
            search();
        });
    }

    // Show only cards in current page
    let start = (current_page-1) * cards_per_page;
    let end = Math.min(current_page * cards_per_page, cards.length - 1);
    if (cards.length <= cards_per_page) {
        cards_page = cards;
    } else {
        cards_page = cards.slice(start, end);
    }

    
    myCards.innerHTML = cards_page.map((card) => { return card.html_card; }).join('');
    
    // Update extra functionality
    add_tooltip();
    add_copy_card();
    add_modals();
}

document.onkeydown = checkKey;

function checkKey(e) {

    if(searchBar === document.activeElement){
        return;
    }
    
    e = e || window.event;

    if (e.keyCode == '37') {
       // left arrow
       current_page--;
       search();
    }
    else if (e.keyCode == '39') {
       // right arrow
       current_page++;
       search();

    }

}

// Change page with swipe gestures for mobiles devices
let touchstartX = 0;
let touchstartY = 0;
let touchendX = 0;
let touchendY = 0;

const gestureZone = document;

gestureZone.addEventListener('touchstart', function(event) {
    touchstartX = event.changedTouches[0].screenX;
    touchstartY = event.changedTouches[0].screenY;
}, false);

gestureZone.addEventListener('touchend', function(event) {
    touchendX = event.changedTouches[0].screenX;
    touchendY = event.changedTouches[0].screenY;
    handleGesture();
}, false); 

function handleGesture() {
    if (touchendX+140 <= touchstartX) {
        console.log('Swiped left');
        current_page++;
        search();
    }
    
    if (touchendX-140 >= touchstartX) {
        console.log('Swiped right');
        current_page--;
        search();
    }
}

loadCardsData();
