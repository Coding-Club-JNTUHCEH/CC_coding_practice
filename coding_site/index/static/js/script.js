// window.addEventListener('DOMContentLoaded', (event) => {
//     console.log('DOM fully loaded and parsed');

//     let tags = [];

//     function addTodo(tagName) {
//         const tag = {
//             tagName,
//             id: Date.now()
//         };
//         tags.push(tag);
//         console.log(tags);
//         renderTodo(tag);
//     }

//     //Select the form element
//     console.log("listOfTags : ");
//     const listOfTags = document.getElementById("listOfTags");

//     console.log("tags: " + listOfTags);




//     //Add a submit event listener
//     document
//         .querySelector('#listOfTags')
//         .addEventListener('change', addBox);

//     function addBox() {
//         //to prevent the page from loading
//         event.preventDefault();

//         //Select the text input
//         const selectedTag = this.value;
//         console.log("selected tag :", this.value);

//         if (selectedTag !== '') {
//             addTodo(selectedTag);
//         }
//         console.log("listOfTags : ", listOfTags);
//     }


//     function renderTodo(tag) {
//         const displayedTags1 = document.querySelector('.tags');
//         console.log("id-tagsToDisplay: " + tag.id);
//         // select the current todo item in the DOM
//         //const tagToDisplay = document.getElementById('' + tag.id);

//         const node = document.createElement('div');
//         node.setAttribute('id', tag.id);
//         //  node.setAttribute('class', 'displayedTag')
//         node.innerHTML = `

//                 <div> ${tag.tagName}</div>
//                 <button class="deleteTag "><i class="fa fa-trash"></i>  </button>
//         `;
//         console.log(node);
//         displayedTags1.append(node);
//     }


//     //Mark a task as completed

//     // Select the entire list
//     const displayedTags = document.querySelector('.tags');
//     // Add a click event listener to the list and its children
//     displayedTags.addEventListener('click', event => {


//         event.preventDefault();
//         console.log("Event :" + event);

//         if (event.target.classList.contains('deleteTag')) {
//             const tagId = event.target.parentNode.id;
//             console.log("delete - " + event.target.parentNode.id);
//             console.log("delete : " + tagId);
//             deleteTag(tagId);
//         }
//     });







//     function deleteTag(tagId) {

//         console.log("inside delete tag");
//         // find the corresponding todo object in the todoItems array
//         const index = tags.findIndex(tagl => tagl.id === Number(tagId));
//         // Create a new object with properties of the current todo item
//         // and a `deleted` property which is set to true
//         const deletedTag = {
//             deleted: true,
//             ...tags[index]
//         };
//         document.getElementById(tagId).classList.add('remove');
//         document.getElementById(tagId).remove();
//         tags = tags.filter(tagl => tagl.id !== Number(tagId));
//         console.log("tags - ");
//         for (var t in tags) {
//             console.log(tags[t]);
//         }
//         // remove the todo item from the array by filtering it out
//         // document.getElementById(tagId).addEventListener("transitionend", function () {
//         //     console.log("delte!!!!")


//         //     console.log("deleted!!:)")
//         // });


//     }

//     // document.querySelector('#submit').addEventListener('click', function () {

//     //     $.ajax({
//     //         type: 'POST',
//     //         url: '/dasboard',
//     //         data: { 'tags': tags },
//     //     });
//     //     console.log(tags);
//     // });

//     // $(".listOfTags").chosen({
//     //     no_results_text: "Oops, nothing found!"
//     // })
//     // $('#listOfTags').multiselect({
//     //     width: '230px',
//     //     defaultText: 'Select Below', height: '250px'
//     // });

//     // $(document).ready(function (e) {
//     //     $('.selectpicker').selectpicker();
//     // });


// });

////////////////////////     PAGINATION     ///////////////////////


