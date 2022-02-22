
// Hide all non general data if no media format is given
// reveal neccessary data depending on selection
var allFields = [
    "text", "correct", "feedback_correct", "feedback_incorrect", "ranking_position", "subsequences",
    "feedback_subsequences", "range_value", "range_max", "range_min", "range_step", "tolerance"
];

let qTypeFields = {
    "SC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "MC": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "TF": ["text", "correct", "feedback_correct", "feedback_incorrect"],
    "RN": ["text", "feedback_correct", "feedback_incorrect", "ranking_position", "subsequences", "feedback_subsequences"],
    "RG": ["range_value", "range_max", "range_min", "range_step", "tolerance", "feedback_correct", "feedback_incorrect",],
    "": allFields
};

function hide(field){
    $("td.field-".concat(field)).hide();
    $("th.column-".concat(field)).hide();
}

function show(field){
    $("td.field-".concat(field)).show();
    $("th.column-".concat(field)).show();
}

function hideAllFields(){
    allFields.forEach(hide);
}

function showFields(fieldType){
    hideAllFields();
    qTypeFields[fieldType].forEach(show);
}


$(document).ready( function() {
    let q_type = $("select[name=type]").val();
    $('#id_type').change(function(){
        showFields($(this).val());
        q_type = $("select[name=type]").val();
    });
    showFields(q_type);
});
