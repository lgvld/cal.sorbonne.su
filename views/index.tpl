<!doctype html>
<html lang="fr">
<head>
<title>{{ title }}</title>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<!-- <link href="static/css/style.css" rel="stylesheet"> -->
<link href="static/css/style.min.css" rel="stylesheet">
</head>
<body>

<div id="wrapper">

<div id="menu">
<ul>
% for master in masters:
% if master in selected_masters:
<li><a href="{{ master }}" class="selected">{{ master }}</a></li>
% else:
<li><a href="{{ master }}">{{ master }}</a></li>
% end
% end
</ul>
</div>

<table id="events">
<thead>
<tr>
<th>🎪 what?</th>
<th>🪂 where?</th>
<th>⏳ when?</th>
</tr>
</thead>
<tbody>
% for event in events:
<tr>
<td>{{ event.name }}</td>
<td>{{ event.location if event.location else "-" }}</td>
<td>{{ event.begin.format('YYYY-MM-DD HH:mm') }} ({{ event.begin.humanize(locale="en") }})</td>
</tr>
%end
</tbody>
</table>

</div>

<!-- <script src="static/js/index.umd.min.js"></script> -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pulltorefreshjs/0.1.20/index.umd.min.js" integrity="sha512-P5gzVTkY5AyMpwWEMaX9lnqzRdVF1x+YjUeAmOT+xGVxhe28aJz4qHZEY+HyTNcs4Xmt89D/wbCltIvSTzlscA==" crossorigin="anonymous"></script>
<script>

// const ptr = PullToRefresh.init({
//   mainElement: 'body',
//   onRefresh() {
//     window.location.reload();
//   }
// });

function toggleMenu() {
  if (window.location.hash == "#hide-menu") {
    document.querySelector("#wrapper").style.gridTemplateColumns = "1fr";
    document.querySelector("#menu").style.display = "none";
  } else {
    document.querySelector("#wrapper").style.gridTemplateColumns = "1fr 4fr";
    document.querySelector("#menu").style.display = "block";
  }
}

toggleMenu();

window.onhashchange = toggleMenu;

</script>

</body>
</html>
