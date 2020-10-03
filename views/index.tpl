<!doctype html>
<html lang="fr">
<head>
<title>{{ title }}</title>
<meta charset="utf-8">
<meta name="robots" content="noindex">
<link href="static/css/style.css" rel="stylesheet">
</head>
<body>

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
<th>⏰ ok... but when?</th>
</tr>
</thead>
<tbody>
% for event in events:
<tr>
<td>{{ event.name }}</td>
<td>{{ event.location if event.location else "-" }}</td>
<td>{{ event.begin.humanize(locale="en") }}</td>
<td>{{ event.begin.format('YYYY-MM-DD HH:mm') }}</td>
</tr>
%end
</tbody>
</table>

<script src="static/js/index.umd.min.js"></script>
<script>
const ptr = PullToRefresh.init({
  mainElement: 'body',
  onRefresh() {
    window.location.reload();
  }
});
</script>

</body>
</html>
