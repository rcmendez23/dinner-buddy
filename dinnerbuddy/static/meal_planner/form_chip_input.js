/* Spectre form autocomplete input Javascript */

$(document).ready(() => {
    const input = $(".form-autocomplete-input .form-chip-input");
    let clearBtn = $(".btn-clear");

    // when value entered, add chip
    input.keypress(function (event) {
        let arr = [];
        let keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode === 13) {
            event.preventDefault();
            arr.push('<div class=\"chip\">');
            arr.push($(this).val());
            arr.push('<a class=\"btn btn-clear\" aria-label=\"Close\" role=\"button\"></a>');
            arr.push('</div>');
            $(this).before(arr.join(''));

            // clear the input field once text has been entered
            $(this).val("");

            // Add event handler to new x buttons
            clearBtn = $(".btn-clear");
            clearBtn.click((e) => {
                $(e.target).parent().remove();
            })
        }
    });

    // Handle x button click
    clearBtn.click((e) => {
        $(e.target).parent().remove();
    })

});