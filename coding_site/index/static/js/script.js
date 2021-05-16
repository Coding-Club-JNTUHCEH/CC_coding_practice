
let tags = [];

function addTodo(tagName) {
    const tag = {
        tagName,
        id: Date.now()
    };
    tags.push(tag);
    console.log(tags);
    renderTodo(tag);
}

//Select the form element
console.log("listOfTags : ");
const listOfTags = document.getElementById("listOfTags");

console.log("tags: " + listOfTags);




//Add a submit event listener
document
    .querySelector('#list')
    .addEventListener('change', addBox);

function addBox() {
    alert("yeah");

    // event.preventDefault();

    // //Select the text input
    // const selectedTag = this.value;
    // console.log("selected tag :", this.value);

    // if (selectedTag !== '') {
    //     addTodo(selectedTag);
    //     selectedTag.value = '';
    //     selectedTag.focus();
    // }
    // console.log("listOfTags : ", listOfTags);
}


function renderTodo(tag) {
    const displayedTags1 = document.querySelector('.tags');
    console.log("id-tagsToDisplay: " + tag.id);
    // select the current todo item in the DOM
    //const tagToDisplay = document.getElementById('' + tag.id);

    const node = document.createElement('div');
    node.setAttribute('id', tag.id);
    node.setAttribute('class', 'displayedTags1')
    node.innerHTML = `
        <div class="tagName"  id="tag-${tag.id}">
                <div> ${tag.tagName}</div>
                <button class="deleteTag "><i class="fa fa-trash"></i>  </button>
        </div> 
        `;
    console.log(node);
    displayedTags1.append(node);
}


//Mark a task as completed

// Select the entire list
const displayedTags = document.querySelector('.tags');
// Add a click event listener to the list and its children
displayedTags.addEventListener('click', event => {

    console.log("Event :" + event);

    if (event.target.classList.contains('deleteTag')) {
        const tagId = event.target.parentNode.id;
        console.log("delete - " + event.target.parentNode.id);
        console.log("delete : " + tagId);
        deleteTag(tagId);
    }
    else if (event.target.parentNode.classList.contains('deleteTag')) {
        const tagId = event.target.parentNode.parentNode.id;
        console.log("delete - " + event.target.parentNode.parentNode.id);
        console.log("delete : " + tagId);
        deleteTag(tagId);
    }
});







function deleteTag(tagId) {
    // find the corresponding todo object in the todoItems array
    const index = tags.findIndex(tag => tag.id === Number(tagId));
    // Create a new object with properties of the current todo item
    // and a `deleted` property which is set to true
    const deletedTag = {
        deleted: true,
        ...tags[index]
    };
    document.getElementById(tagId).classList.add('remove');
    // remove the todo item from the array by filtering it out
    document.getElementById(tagId).addEventListener("transitionend", function () {
        document.getElementById(tagId).remove();
        tags = tags.filter(tag => tag.id !== Number(tagId));
    });


}