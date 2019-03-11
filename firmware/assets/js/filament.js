var time_elapsed = 0;
function finish_load_filament() {
    alert("finish")
}

function load_filament_wait() {
    ++time_elapsed;
    var perc = Math.round((time_elapsed/66)*100);
    if(time_elapsed == 100){
        finish_load_filament()
    } else {
        $('#progress_bar').attr("value", perc);
        setTimeout(load_filament_wait, 1000);
    }
}


