document.addEventListener("DOMContentLoaded", function() {
    const checkboxes = document.querySelectorAll(".checkbox");

    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener("click", function() {
            if (checkbox.checked) {
                console.log(checkbox.name + " is checked");
            } else {
                console.log(checkbox.name + " is unchecked");
            }
        });
    });
});


