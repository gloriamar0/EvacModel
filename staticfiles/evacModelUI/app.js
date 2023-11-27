// Mapping disaster choices to city options
var choices = {
    'Houston': ['Fire', 'Flooding', 'Hurricane', 'Explosion'],
    'College Station': ['Fire', 'Flooding', 'Explosion'],
    'Lahaina': ['Fire', 'Flooding', 'Tsunami', 'Explosion']
};

// Changing options when city is selected
$('#cities').on('change', function() {
    var selectedCity = $(this).val();
    var disasterChoices = choices[selectedCity];
    $('#event').empty();

    for (i = 0; i < disasterChoices.length; i++) {
        $('#event').append("<option value='" + disasterChoices[i] + "'>" + disasterChoices[i] + "</option>");
    }
});