var l_un = document.getElementById('l_un');
var r_un = document.getElementById('r_un');

if (l_un)
  l_un.onclick = function() {
    alert('Already the first page!');
  }
if (r_un)
  r_un.onclick = function() {
    alert('Already the last page!');
  }
