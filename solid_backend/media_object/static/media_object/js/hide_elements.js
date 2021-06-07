
const img_rows = [
    ".fieldBox.field-dzi_option", ".form-row.field-img_alt", ".form-row.field-dzi_file",
    ".form-row.field-img_original_width", ".form-row.field-img_original_height",
    ".form-row.field-length_value.field-length_unit.field-pixel_number",
        ".form-row.field-img_original_scale", ".form-row.field-audio",
    ".form-row.field-audio_duration",
];

const audio_video_rows = [".form-row.field-media_duration"];

const non_general_data = img_rows.concat(audio_video_rows);

function hide(i) {
    $(i).hide();
}

function fadeout(i) {
    $(i).hide(1000);
}
function show(i) {
    $(i).show(1000);
}
function hide_data(data) {
    data.forEach(hide)
}

function checkFields(old_media_format) {

    var media_format = $("input[type='radio'][name='media_format']:checked").val();

    if (media_format == "image") {
        if (old_media_format == "audio" || old_media_format == "video"){
            audio_video_rows.forEach(fadeout)
            img_rows.forEach(show);
        }
        else {
            img_rows.forEach(show);
        }

    }
    else if (media_format == "audio" || media_format == "video") {
        if (old_media_format == "audio" || old_media_format == "video") {
            audio_video_rows.forEach(show);
        }
        else if (old_media_format == "image") {
            img_rows.forEach(fadeout);
            audio_video_rows.forEach(show);
        }
        else {
            audio_video_rows.forEach(show);
        }
    }
}

// Hide all non general data if no media format is given
// reveal neccessary data depending on selection

$(document).ready( function() {
    var prev = $("input[type='radio'][name='media_format']:checked").val();

    hide_data(non_general_data);

    $('#id_media_format').change(function(){
        checkFields(prev);
        prev = $("input[type='radio'][name='media_format']:checked").val();
    });

    checkFields(prev);

});
