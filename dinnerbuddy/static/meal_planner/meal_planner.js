$(document).ready(() => {
    // on form submit
    const form = $("form");
    form.submit((e) => {
        const inputs = $(".form-chip-input")

        // go thru each input to get the chip values
        inputs.each((i, input) => {
            const chips = $(input).parent().find(".chip");
            console.log(chips)
            let arr = [];
            chips.each((i, chip) => {
                console.log(chip);
                arr.push($(chip).text());
            });

            // set the input value (so it can be passed in the get request)
            $(input).val(arr.join(", "));
            console.log($(input).val());
        })
    });
});