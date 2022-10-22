function add_modals() {
    cards_icons_list = document.getElementsByClassName('ref-repo-icons');
    for(const cards_icons of cards_icons_list){
        for(const card_icon of cards_icons.children){
            const icon = card_icon.getElementsByClassName('icon')[0];
            const modal = card_icon.getElementsByClassName('modal')[0];
            const modal_content = card_icon.getElementsByClassName('modal-content')[0];
            const span_close = card_icon.getElementsByClassName('close')[0];
            
            if (modal != undefined){
                icon.addEventListener('click', () => { 
                    modal.classList.add('modal-on');
                });
                span_close.addEventListener('click', () => { 
                    modal.classList.remove('modal-on');
                });
                modal_content.addEventListener('click', (event) => { 
                    event.stopPropagation();
                });
                modal.addEventListener('click', () => { 
                    modal.classList.remove('modal-on');

                });
            }
        }
        
        const license = cards_icons.getElementsByClassName('ref-license')[0];
        if (license != undefined) {
            license.addEventListener('click', () => { 
                getGithub(license);
            });
        }
        
    }
    const descriptions = document.getElementsByClassName('description');
    [].forEach.call(descriptions, function (description) {
        if (isOverflown(description)) {
            description.style.cursor="pointer";
            const modal = description.getElementsByClassName('modal')[0];
            const modal_content = description.getElementsByClassName('modal-content')[0];
            const span_close = description.getElementsByClassName('close')[0];
            if (modal != undefined){
                description.addEventListener('click', () => { 
                    modal.classList.add('modal-on');
                });
                span_close.addEventListener('click', () => { 
                    modal.classList.remove('modal-on');
                });
                modal_content.addEventListener('click', (event) => { 
                    event.stopPropagation();
                });
                modal.addEventListener('click', (event) => { 
                    modal.classList.remove('modal-on');
                    event.stopPropagation();
                });
            }
        }
    });
    const ontologies = document.getElementsByClassName('m_ontology');
    [].forEach.call(ontologies, function (ontology) {
            const modal = ontology.getElementsByClassName('modal')[0];
            const modal_content = ontology.getElementsByClassName('modal-content')[0];
            const span_close = ontology.getElementsByClassName('close')[0];
            if (modal != undefined){
                ontology.addEventListener('click', () => { 
                    modal.classList.add('modal-on');
                });
                span_close.addEventListener('click', () => { 
                    modal.classList.remove('modal-on');
                });
                modal_content.addEventListener('click', (event) => { 
                    event.stopPropagation();
                });
                modal.addEventListener('click', (event) => { 
                    modal.classList.remove('modal-on');
                    event.stopPropagation();
                });
            }
    });
    
}

function isOverflown(element) {
    return element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth;
}

function addList(element, iterable){
    var list = document.createElement("ol");
        for (let i of iterable) {
            let item = document.createElement("li");
            item.innerHTML = i.charAt(0).toUpperCase() + i.slice(1);
            list.appendChild(item);
        }
        element.innerHTML = '';
        element.appendChild(list);
}

async function getGithub(license){
    if (license.dataset.url != 'None'){
        const response = await fetch(license.dataset.url);
        const response_aux = response.clone();
        try {
            const data =  await response.json();

            const name = license.getElementsByClassName('ref-name')[0];
            const description = license.getElementsByClassName('ref-description')[0];
            const permissions = license.getElementsByClassName('ref-permissions')[0];
            const conditions = license.getElementsByClassName('ref-conditions')[0];
            const limitations = license.getElementsByClassName('ref-limitations')[0];

            name.innerHTML = await data.name;
            description.innerHTML = await data.description;

            addList(permissions, data.permissions);
            addList(conditions, data.conditions);
            addList(limitations, data.limitations);

        } catch (error) {
            const description = license.getElementsByClassName('ref-description-aux')[0];
            description.innerHTML = '<pre style="font-family: monospace;">'+await response_aux.text()+'</pre>';
        }
    } else console.log('No license.');
}