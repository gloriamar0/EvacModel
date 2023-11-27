// Mapping disaster choices to city options
var choices = {
    'Houston': ['Fire', 'Flooding', 'Hurricane', 'Explosion'],
    'College Station': ['Fire', 'Flooding', 'Explosion'],
    'Lahaina': ['Fire', 'Flooding', 'Tsunami', 'Explosion'],
};

var population = {
    'Houston': '~2,300,000',
    'College Station': '~124,000',
    'Lahaina': '~13,300',
};

// Changing options when city is selected
$('#cities').on('change', function() {
    var selectedCity = $(this).val();
    // alert(population[selectedCity]);
    $('#event').empty();
    $('#event').append("<option value='' selected disabled>Choose...</option>");

    for (i = 0; i < choices[selectedCity].length; i++) {
        $('#event').append("<option value='" + choices[selectedCity][i] + "'>" + choices[selectedCity][i] + "</option>");
    }

    // document.getElementById("populationDisplay").textContent = population[selectedCity];
});