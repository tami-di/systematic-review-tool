const searchWrapper = document.querySelector(".search-input");
const inputBox = searchWrapper.querySelector("input");
const suggBox = searchWrapper.querySelector(".autocom-box");
const icon = searchWrapper.querySelector(".icon");
let linkTag = searchWrapper.querySelector("a");

inputBox.onkeyup = (e) => {
    let userData = e.target.value; // user entered data

    if (userData) {
        // Make an AJAX request to fetch suggestions from the backend
        fetch(`/getSuggestions?input=${userData}`)
            .then((response) => response.json())
            .then((data) => {
                let emptyArray = data.suggestions; // Assuming the response contains suggestions in a 'suggestions' field

                if (emptyArray.length > 0) {
                    emptyArray = emptyArray.map((data) => {
                        return '<li>' + data + '</li>';
                    });
                    searchWrapper.classList.add("active");
                    showSuggestions(emptyArray);
                    let allList = suggBox.querySelectorAll("li");
                    for (let i = 0; i < allList.length; i++) {
                        allList[i].setAttribute("onclick", "select(this)");
                    }
                } else {
                    searchWrapper.classList.remove("active");
                }
            })
            .catch((error) => {
                console.error('Error fetching suggestions:', error);
            });
    } else {
        searchWrapper.classList.remove("active");
    }
};

function select(element) {
    let selectData = element.textContent;
    inputBox.value = selectData;
    searchWrapper.classList.remove("active");
}

function showSuggestions(list) {
    let listData;
    if (!list.length) {
        userValue = inputBox.value;
        listData = '<li>' + userValue + '<li>';
    } else {
        listData = list.join('');
    }
    suggBox.innerHTML = listData;
}
