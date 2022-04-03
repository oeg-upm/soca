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