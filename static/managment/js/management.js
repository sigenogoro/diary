
var move_flg = "";
var move_start_x = 0;
var move_start_y = 0;
// start drag
window.onmousedown = function(e) {
  move_flg = "true";
  move_start_x = event.clientX - parseInt(document.getElementById("ajax_task").style.left.replace("px",""));
  move_start_y = event.clientY - parseInt(document.getElementById("ajax_task").style.top.replace("px",""));
}
// end drag
window.onmouseup = function(e) {
  move_flg = "false";
}
// dræg
window.onmousemove = function(e) {
  if(move_flg == "true") {
    document.getElementById("ajax_task").style.left = (event.clientX - move_start_x) + "px";
    document.getElementById("ajax_task").style.top = (event.clientY - move_start_y) + "px";
  }
}